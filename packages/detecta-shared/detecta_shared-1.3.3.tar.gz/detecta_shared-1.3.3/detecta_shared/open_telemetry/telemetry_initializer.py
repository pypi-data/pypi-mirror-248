from detecta_shared.loggers.log_initializer import LogInitializerByConfig
from detecta_shared.open_telemetry.metrics_intializer_base import MetricsInitializerBase
from detecta_shared.open_telemetry.tracing_initializer_base import TracingInitializerBase


class TelemetryInitializer:
    def __init__(self, logger_initializer: LogInitializerByConfig, tracing_initializer: TracingInitializerBase,
                 metrics_initializer: MetricsInitializerBase):
        self.tracing_initializer = tracing_initializer
        self.logger_initializer = logger_initializer
        self.metrics_initializer = metrics_initializer

    def init(self):
        self.logger_initializer.init_logger()
        self.metrics_initializer.init_metrics()
        self.tracing_initializer.init_tracing()
