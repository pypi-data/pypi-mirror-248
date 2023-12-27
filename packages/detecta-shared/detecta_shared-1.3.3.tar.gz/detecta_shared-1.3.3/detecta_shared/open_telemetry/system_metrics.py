import psutil
from opentelemetry import metrics
from opentelemetry.metrics import CallbackOptions, Observation


class SystemMetrics:
    def __init__(self):
        self._is_observe = False
        meter = metrics.get_meter(__name__)
        self._current_process = psutil.Process()
        self._memory_usage_gauge = meter.create_observable_gauge("memory_usage",
                                                                 callbacks=[self._get_memory_usage], unit="megabytes")
        self._cpu_usage = meter.create_observable_gauge("cpu_usage", callbacks=[self._get_cpu_usage], unit="percents")

    def _get_memory_usage(self, _: CallbackOptions):
        if self._is_observe:
            memory_info = self._current_process.memory_info()
            memory_used = memory_info.rss
            memory_used_mb = memory_used / (1024 * 1024)
            yield Observation(memory_used_mb)
        else:
            yield Observation(0)

    def _get_cpu_usage(self, _: CallbackOptions):
        if self._is_observe:
            yield Observation(self._current_process.cpu_percent())
        else:
            yield Observation(0)

    def instrument(self):
        self._is_observe = True
