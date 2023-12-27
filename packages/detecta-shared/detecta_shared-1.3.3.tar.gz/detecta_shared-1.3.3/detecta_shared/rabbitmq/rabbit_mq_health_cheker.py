from opentelemetry import metrics
from opentelemetry.metrics import CallbackOptions, Observation

from detecta_shared.rabbitmq.rabbitmq_event_listener import RabbitmqEventListener
from detecta_shared.rabbitmq.rabbitmq_publisher import RabbitMQPublisher


class RabbitMQHealthChecker:
    def __init__(self, publisher: RabbitMQPublisher, listener: RabbitmqEventListener):
        self.listener = listener
        self._publisher = publisher
        meter = metrics.get_meter(__name__)
        self._health_status_metric = meter.create_observable_gauge(name="rabbit_mq_healthcheck_status",
                                                                   callbacks=[self._check],
                                                                   unit="1",
                                                                   description="rabbitmq_healthcheck_status")

    def is_healthy(self) -> bool:
        return self._publisher.is_healthy() and self.listener.is_healthy()

    def _check(self, _: CallbackOptions):
        if self.is_healthy():
            yield Observation(1)
        else:
            yield Observation(0)
