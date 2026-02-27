from kubernetes import client, config
import os


class KubernetesAdapter:

    def __init__(self):

        try:
            if os.getenv("KUBERNETES_SERVICE_HOST"):
                config.load_incluster_config()
            else:
                config.load_kube_config()

            self.v1 = client.CoreV1Api()
            self.available = True

        except Exception:
            self.available = False


    def get_pod_health(self):

        if not self.available:
            return self._mock_health()

        pods = self.v1.list_pod_for_all_namespaces()

        unhealthy = 0
        total = 0

        for pod in pods.items:

            total += 1

            for c in pod.status.container_statuses or []:
                if not c.ready:
                    unhealthy += 1

        return {
            "total_pods": total,
            "unhealthy_pods": unhealthy
        }


    def _mock_health(self):

        import random

        return {
            "total_pods": 24,
            "unhealthy_pods": random.randint(0, 4)
        }