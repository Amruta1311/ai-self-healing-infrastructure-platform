import numpy as np
from collections import deque


class AnomalyDetector:

    def __init__(self, window=40):

        self.hist = {
            "cpu": deque(maxlen=window),
            "memory": deque(maxlen=window),
            "latency": deque(maxlen=window),
            "errors": deque(maxlen=window)
        }


    def update(self, metrics):

        for k in self.hist:
            self.hist[k].append(metrics[k])


    def _z(self, series, val):

        if len(series) < 10:
            return 0

        return (val - np.mean(series)) / (np.std(series) + 1e-6)


    def detect(self, metrics):

        self.update(metrics)

        anomalies = {}

        for k in self.hist:

            z = self._z(self.hist[k], metrics[k])

            if abs(z) > 2.3:
                anomalies[k] = round(z, 2)

        return anomalies