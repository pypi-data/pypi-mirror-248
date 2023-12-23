from prometheus_client import Histogram, start_http_server

from stsdk.utils.config import config


class Metric:
    def __init__(self, port):
        self.histogram = Histogram(
            "processing_time_seconds",
            "Time spent processing",
            labelnames=["kind", "operation"],
        )
        start_http_server(port)

    def MetricTime(self, kind, operation, start_time, end_time):
        self.histogram.labels(kind=kind, operation=operation).observe(
            end_time - start_time
        )


metric = Metric(config.metirc_port)
