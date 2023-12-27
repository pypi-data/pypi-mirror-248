import logging
import threading
import time
from typing import Optional

import jsonpickle
import pika
from opentelemetry import trace
from opentelemetry.trace import SpanKind
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ConnectionClosed

from detecta_shared.abstractions.integration_events import IntegrationEvent
from detecta_shared.rabbitmq.rabbit_mq_metrics import RabbitMQPublishMetrics
from detecta_shared.rabbitmq.rabbitmq_connection import RabbitMQConnection
from detecta_shared.rabbitmq.rabbitmq_params import RabbitMQPublisherParams, RabbitMQSendParams

tracer = trace.get_tracer(__name__)

class PublishResult:
    def __init__(self, event: threading.Event):
        self._event = event
        self._error: Optional[Exception] = None

    def mark_ended(self):
        self._event.set()

    def set_error(self, error: Exception):
        self._error = error

    def raise_error_if_exists(self):
        if self._error:
            raise self._error


class RabbitMQPublisher(threading.Thread):

    def __init__(self, params: RabbitMQPublisherParams, connection: RabbitMQConnection, logger: logging.Logger):
        super().__init__(daemon=True)
        self._rabbit_metrics = RabbitMQPublishMetrics()
        self._logger = logger
        self._connection = connection
        self._publisher_params = params
        self._channel: Optional[BlockingChannel] = None
        self.start()

    def run(self) -> None:
        while True:
            try:
                if not self._connection.is_connected():
                    self._connection.try_connect()
                self._connection.connection.process_data_events(time_limit=0.15)
            except Exception as ex:
                self._logger.warning(f"Connection rabbit publisher failed, reconnecting... Error: {ex}")
                time.sleep(3)

    def _publish(self, event: IntegrationEvent, message_params: RabbitMQSendParams, result: PublishResult,
                 headers: dict):
        try:
            if not self._channel or self._channel.is_closed:
                self._channel = self._connection.create_channel()
                self._logger.info(f"Channel RabbitMQ created to send: {type(event).__name__}")

            body = jsonpickle.dumps(event, unpicklable=False).encode()
            live_time = None
            if message_params.message_live_milliseconds:
                live_time = str(message_params.message_live_milliseconds)
            self._logger.info(f"Publishing to RabbitMQ {type(event).__name__}")
            headers['message_send_time'] = str(time.time())
            self._channel.basic_publish(exchange=self._publisher_params.exchange,
                                        routing_key=message_params.routing_key,
                                        body=body, properties=pika.BasicProperties(delivery_mode=2,
                                                                                   expiration=live_time,
                                                                                   headers=headers))
            self._rabbit_metrics.rabbitmq_messages_published.add(1)
        except Exception as ex:
            result.set_error(ex)
            self._rabbit_metrics.rabbitmq_messages_published_with_error.add(1)
        finally:
            result.mark_ended()

    def is_healthy(self):
        return self._connection.is_connected()

    def publish(self, event: IntegrationEvent, message_params: RabbitMQSendParams):
        self._add_publish_callback(event, message_params, 0)

    # Делаем такой метод и callback потому что если мы будем отправлять с другого потока, будет разрыв connection
    # Это все связано с heartbeat, если обработка сообщения будет долгая, то шанс на разрыв увеличится
    def _add_publish_callback(self, event: IntegrationEvent, message_params: RabbitMQSendParams, retry_count: int):
        try:
            callback_event = threading.Event()
            publish_result = PublishResult(callback_event)
            with tracer.start_as_current_span("rabbitmq_publish", kind=SpanKind.PRODUCER) as span:
                span.set_attribute("message", type(event).__name__)
                propagator = TraceContextTextMapPropagator()
                carrier = {}
                propagator.inject(carrier)
                self._connection.connection.add_callback_threadsafe(lambda: self._publish(event, message_params,
                                                                                          publish_result,
                                                                                          carrier))
                callback_event.wait()
                publish_result.raise_error_if_exists()
        except (pika.exceptions.AMQPChannelError, pika.exceptions.AMQPConnectionError) as ex:
            if retry_count > 10:
                raise
            self._logger.warning(
                f"Can't send message to rabbitmq error: {ex}, trying again, retry count: {retry_count}")
            if not self._connection.is_connected():
                self._connection.try_connect()
            self._add_publish_callback(event, message_params, retry_count + 1)
