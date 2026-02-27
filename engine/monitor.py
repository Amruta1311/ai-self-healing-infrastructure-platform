import random
import time

def generate_metrics():
    cpu = random.uniform(20, 95)
    memory = random.uniform(30, 90)
    latency = random.uniform(50, 800)

    return {
        "cpu": round(cpu, 2),
        "memory": round(memory, 2),
        "latency": round(latency, 2),
        "timestamp": time.time()
    }


def generate_logs(metrics):
    logs = []

    if metrics["cpu"] > 75:
        logs.append("ERROR: CPU saturation detected")

    if metrics["latency"] > 500:
        logs.append("WARN: High API latency")

    if metrics["memory"] > 85:
        logs.append("ERROR: Memory pressure critical")

    if not logs:
        logs.append("INFO: System stable")

    return logs