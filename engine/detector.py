def detect_anomaly(metrics):
    anomalies = []

    if metrics["cpu"] > 75:
        anomalies.append("High CPU")

    if metrics["memory"] > 80:
        anomalies.append("High Memory")

    if metrics["latency"] > 400:
        anomalies.append("High Latency")

    return anomalies