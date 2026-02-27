class TelemetryEngine:

    def __init__(self, k8s, prom):
        self.k8s = k8s
        self.prom = prom


    def collect(self):

        infra = self.k8s.get_pod_health()
        metrics = self.prom.query_metrics()

        return {
            "metrics": metrics,
            "infra": infra
        }