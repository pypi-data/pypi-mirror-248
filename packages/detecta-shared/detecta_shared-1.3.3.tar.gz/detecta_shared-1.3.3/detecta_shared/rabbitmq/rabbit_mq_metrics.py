from opentelemetry import metrics


class RabbitMQPublishMetrics:
    def __init__(self):
        meter = metrics.get_meter(__name__)
        self.rabbitmq_messages_published = meter.create_counter("rabbitmq_messages_published",  unit="total")
        self.rabbitmq_messages_published.add(0)
        self.rabbitmq_messages_published_with_error = meter.create_counter("rabbitmq_messages_published_with_error",
                                                                           unit="total")
        self.rabbitmq_messages_published_with_error.add(0)

class RabbitMQListenerMetrics:
    def __init__(self):
        meter = metrics.get_meter(__name__)
        self.rabbitmq_messages_processed = meter.create_counter("rabbitmq_messages_processed",  unit="total")
        self.rabbitmq_messages_processed.add(0)
        self.rabbitmq_messages_processed_with_error = meter.create_counter("rabbitmq_messages_processed_with_error")
        self.rabbitmq_messages_processed_with_error.add(0)
        self.rabbitmq_messages_duration_get_from_queue = meter.create_histogram(
            name="rabbitmq_messages_duration_get_from_queue",
            description="Time difference between a sent message and the time it was received from the queue in ms",
            unit="ms"
        )