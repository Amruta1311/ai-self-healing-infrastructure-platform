import random

class RootCauseAnalyzer:

    def __init__(self):
        self.models = {
            "cpu_saturation": {
                "cpu": 0.5,
                "latency": 0.3,
                "errors": 0.2
            },
            "memory_exhaustion": {
                "memory": 0.6,
                "cpu": 0.2,
                "errors": 0.2
            },
            "pod_crash_loop": {
                "unhealthy_pods": 0.7,
                "errors": 0.3
            },
            "db_latency": {
                "latency": 0.6,
                "cpu": 0.1,
                "errors": 0.3
            },
            "network_instability": {
                "errors": 0.5,
                "latency": 0.5
            }
        }

    def analyze(self, anomalies, infra):
        # Randomly pick one failure model
        best = random.choice(list(self.models.keys()))
        weights = self.models[best]

        score = 0
        for signal, w in weights.items():
            print(f'Signal: {signal}, Weight: {w}')

            if signal in anomalies:
                score += abs(anomalies[signal]) * w

            if signal == "unhealthy_pods":
                score += infra.get("unhealthy_pods", 0) * w

        confidence = min(score / 4, 1)

        return {
            "root_cause": best,
            "confidence": round(confidence, 2),
            "scores": {best: score}
        }