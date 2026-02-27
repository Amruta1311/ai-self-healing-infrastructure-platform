class ImpactEstimator:

    def estimate(self, metrics, diagnosis):

        base_sla = 99.95

        penalty = 0

        if metrics["latency"] > 400:
            penalty += 0.02

        if metrics["cpu"] > 85:
            penalty += 0.01

        if diagnosis["confidence"] < 0.7:
            penalty += 0.015

        sla = max(base_sla - penalty, 99.0)

        revenue_loss = round((100 - sla) * 5000, 2)

        return {
            "sla": sla,
            "estimated_loss_usd": revenue_loss
        }