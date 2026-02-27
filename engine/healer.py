class RemediationEngine:

    def __init__(self):

        self.policies = {
            "cpu_overload": self._scale,
            "memory_leak": self._restart,
            "db_bottleneck": self._reroute,
            "network_congestion": self._throttle
        }

    def execute(self, diagnosis):

        cause = diagnosis["root_cause"]
        confidence = diagnosis["confidence"]

        if confidence < 0.6:
            return "Manual review required"

        action = self.policies.get(cause)

        if not action:
            return "No remediation policy"

        return action()

    def _scale(self):
        return "Scaled replicas +1"

    def _restart(self):
        return "Restarted unhealthy pods"

    def _reroute(self):
        return "Shifted traffic to replica DB"

    def _throttle(self):
        return "Applied rate limiting"