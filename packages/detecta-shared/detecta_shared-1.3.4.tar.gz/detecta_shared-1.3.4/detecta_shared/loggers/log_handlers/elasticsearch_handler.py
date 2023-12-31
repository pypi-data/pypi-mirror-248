import logging
import queue
import threading
import time
import uuid
from datetime import datetime

from elasticsearch import Elasticsearch
from opentelemetry import context, trace


class ElasticsearchHandler(logging.Handler):
    def __init__(self, es: Elasticsearch, application_name: str, index_prefix: str, instance_id: str):
        super().__init__()
        self.instance_id = instance_id
        self.index_prefix = index_prefix
        self.application_name = application_name
        self.es = es
        self._logs_queue = queue.Queue()
        threading.Thread(target=self._start_send_events).start()

    def emit(self, record):
        try:
            date = datetime.utcnow()
            index = f"{self.index_prefix}-{date.strftime('%Y.%m.%d')}"
            level = self.log_levels[record.levelname]
            log_data = {
                "@timestamp": date.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                "level": level,
                "ApplicationName": self.application_name,
                "Instance": self.instance_id,
                "message": record.getMessage(),
            }
            trace_id = trace.get_current_span().get_span_context().trace_id
            if trace_id != 0:
                log_data['trace_id'] = uuid.UUID(int=trace_id).hex
            self._logs_queue.put((index, log_data))
        except Exception as ex:
            print(f"Can' t send elastic log.  Ex: {ex}")

    log_levels = {
        "DEBUG": "Debug",
        "INFO": "Information",
        "WARNING": "Warning",
        "ERROR": "Error",
        "CRITICAL": "Fatal"
    }

    def _start_send_events(self):
        while True:
            try:
                if self._logs_queue.empty():
                    time.sleep(2)
                    continue
                try:
                    log = self._logs_queue.get()
                    self.es.index(index=log[0], body=log[1])
                except Exception as ex:
                    print(f"Can' t send elastic log.  Ex: {ex}")
                    self._logs_queue.put(log)
            except Exception as ex:
                print(ex)
