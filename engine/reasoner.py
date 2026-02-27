def reason(anomalies, logs):
    if "High CPU" in anomalies:
        return {
            "cause": "Traffic spike causing CPU exhaustion",
            "confidence": 0.87,
            "fix": "scale_up"
        }

    if "High Memory" in anomalies:
        return {
            "cause": "Memory leak in service",
            "confidence": 0.82,
            "fix": "restart_pod"
        }

    if "High Latency" in anomalies:
        return {
            "cause": "Database bottleneck",
            "confidence": 0.78,
            "fix": "reroute_traffic"
        }

    return {
        "cause": "System healthy",
        "confidence": 0.95,
        "fix": "none"
    }