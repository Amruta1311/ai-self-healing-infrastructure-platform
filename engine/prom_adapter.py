from prometheus_api_client import PrometheusConnect
import os
import random


class PrometheusAdapter:

    def __init__(self):

        url = os.getenv("PROMETHEUS_URL")

        if url:
            try:
                self.client = PrometheusConnect(url=url)
                self.available = True
            except:
                self.available = False
        else:
            self.available = False


    def query_metrics(self):

        if not self.available:
            return self._mock_metrics()

        cpu = self.client.custom_query(
            'avg(rate(container_cpu_usage_seconds_total[2m]))'
        )[0]["value"][1]

        memory = self.client.custom_query(
            'avg(container_memory_working_set_bytes)'
        )[0]["value"][1]

        latency = self.client.custom_query(
            'histogram_quantile(0.95, http_request_duration_seconds_bucket)'
        )[0]["value"][1]

        errors = self.client.custom_query(
            'sum(rate(http_requests_total{status=~"5.."}[1m]))'
        )[0]["value"][1]

        return {
            "cpu": float(cpu) * 100,
            "memory": float(memory) / 1e9,
            "latency": float(latency) * 1000,
            "errors": float(errors)
        }


    def _mock_metrics(self):

        return {
            "cpu": random.uniform(20, 95),
            "memory": random.uniform(2, 16),
            "latency": random.uniform(80, 900),
            "errors": random.uniform(0, 12)
        }