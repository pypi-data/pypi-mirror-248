import abc


class MetricsInitializerBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def init_metrics(self):
        pass

    @staticmethod
    def _get_bool(value):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value in ['true', '1', 'True']
        return False
