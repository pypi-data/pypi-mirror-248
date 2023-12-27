import logging
import threading
import time
import uuid
from typing import Dict, List, Optional

from opentelemetry import context, trace
from opentelemetry.trace import SpanKind
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import AMQPConnectionError, AMQPChannelError
import jsonpickle

from detecta_shared.abstractions.integration_events import IntegrationEvent

from detecta_shared.rabbitmq.rabbit_mq_metrics import RabbitMQListenerMetrics
from detecta_shared.rabbitmq.rabbitmq_connection import RabbitMQConnection
from detecta_shared.rabbitmq.rabbitmq_params import RabbitMQListenerParams
from detecta_shared.rabbitmq.subscription_manager import SubscriptionManager

tracer = trace.get_tracer(__name__)

class RabbitmqEventListener(threading.Thread):
    def __init__(self, subscription_manager: SubscriptionManager, params: RabbitMQListenerParams,
                 connection: RabbitMQConnection, logger: logging.Logger):
        self._connection = connection
        self._subscription_manager = subscription_manager
        self._rabbit_params = params
        self._logger = logger
        self._listening_enabled = True
        self._channel: Optional[BlockingChannel] = None
        self._lock = threading.Lock()
        self._is_listening = False
        self._metrics = RabbitMQListenerMetrics()
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        self._listening_enabled = True
        while self._listening_enabled:
            try:
                if not self._channel or self._channel.is_closed:
                    self._channel = self._connection.create_channel()
                    self._configure_queue(self._subscription_manager.get_all_events())
                self._channel.basic_consume(self._rabbit_params.queue, self._on_message)
                self._logger.info("Start listen rabbit events")
                self._is_listening = True
                self._channel.start_consuming()
            except Exception as ex:
                self._is_listening = False
                self._logger.error(f"Listening rabbit events interrupted. Error: {ex}.")
                try:
                    if self._channel and self._channel.is_open:
                        self._channel.close()
                except Exception as ex:
                    self._logger.warning(f"Can't close channel in listener. Error: {ex}. Flashing channel...")
                    self._channel = None
                time.sleep(5)

    def is_healthy(self) -> bool:
        return self._connection.is_connected() and self._is_listening

    def _configure_queue(self, routing_list: List[str]):
        if not self._channel or self._channel.is_closed:
            self._channel = self._connection.create_channel()

        self._channel.exchange_declare(exchange='dlx_exchange', exchange_type='direct', durable=True)
        self._channel.queue_declare(queue="dead_messages_queue",
                                    durable=True)
        self._channel.queue_bind(exchange='dlx_exchange', queue="dead_messages_queue", routing_key='')
        self._channel.exchange_declare(exchange=self._rabbit_params.exchange,
                                       exchange_type=self._rabbit_params.exchange_type,
                                       durable=True,
                                       )
        self._channel.queue_declare(queue=self._rabbit_params.queue, exclusive=False, durable=True,
                                    arguments={'x-dead-letter-exchange': 'dlx_exchange',
                                               'x-dead-letter-routing-key': ''})
        for routing in routing_list:
            self._channel.queue_bind(self._rabbit_params.queue, self._rabbit_params.exchange, routing)

    def add_event(self, event_name) -> bool:
        self._configure_queue([event_name])
        self._subscription_manager.add_subscription(event_name)
        return True

    def stop_listening(self):
        self._listening_enabled = False
        self._channel.stop_consuming()
        self._logger.info("Rabbit mq listener stopped")

    def _on_message(self, channel: BlockingChannel, method_frame, header_frame, body):
        self._handle_message(channel, method_frame, header_frame, body)

    def _handle_message(self, channel: BlockingChannel, method_frame, header_frame, body):
        try:
            if header_frame.headers is None:
                last_time = time.time()
            else:
                last_time = float(header_frame.headers.get('message_send_time', time.time()))
            calculated_delay = (time.time() - last_time) * 1000
            self._metrics.rabbitmq_messages_duration_get_from_queue.record(calculated_delay)
            event_name = method_frame.routing_key
            event_attributes = jsonpickle.decode(body.decode())
            event = self._map_message(event_name, event_attributes)
            if not self._subscription_manager.has_event_handlers(event_name):
                self._logger.error(f"Can't find event_handler. Routing: {event_name}")
                return
            trace_context = TraceContextTextMapPropagator().extract(header_frame.headers)
            token = context.attach(trace_context)
            try:
                with tracer.start_as_current_span("rabbitmq_processing_message", kind=SpanKind.CONSUMER) as span:
                    span.set_attribute("message", method_frame.routing_key)
                    handlers = self._subscription_manager.get_event_handlers_by_name(event_name)
                    for handler in handlers:
                        handler.handle(event)
                    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            finally:
                context.detach(token)
                self._metrics.rabbitmq_messages_processed.add(1)
        except Exception as ex:
            self._metrics.rabbitmq_messages_processed_with_error.add(1)
            self._reject_message(method_frame.delivery_tag, channel)
            self._handle_error(ex)

    def _reject_message(self, delivery_tag, channel: BlockingChannel):
        try:
            if not self._connection.is_connected() or channel.is_closed:
                self._connection.try_connect()
                self._channel = self._connection.create_channel()
                channel = self._channel
            channel.basic_reject(delivery_tag, False)
        except Exception as ex:
            self._logger.error(f"Can't reject message delivery tag: {delivery_tag}. Error: {ex}", exc_info=ex)

    def _handle_error(self, ex: Exception):
        self._logger.error(f"Can't handle rabbit message. Error: {ex}", exc_info=True)

    @staticmethod
    def _map_message(event_name: str, event_attributes: Dict) -> IntegrationEvent:
        return type(event_name, (object,), event_attributes)


class UUIDHandler(jsonpickle.handlers.BaseHandler):
    def restore(self, obj):
        if isinstance(obj, dict):
            if obj.get("hex", None) is not None:
                obj = obj["hex"]
        return uuid.UUID(obj)

    def flatten(self, obj, data):
        return str(obj)


jsonpickle.handlers.registry.register(uuid.UUID, UUIDHandler)
