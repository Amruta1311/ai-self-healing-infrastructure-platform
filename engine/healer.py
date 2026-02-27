import time

def apply_fix(action):
    if action == "scale_up":
        time.sleep(1)
        return "Scaled cluster nodes"

    if action == "restart_pod":
        time.sleep(1)
        return "Restarted faulty container"

    if action == "reroute_traffic":
        time.sleep(1)
        return "Rerouted traffic to backup zone"

    return "No action needed"