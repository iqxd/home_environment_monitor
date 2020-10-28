import dht


class TempHumi:
    def __init__(self, out):
        self._sensor = dht.DHT11(out)

    def measure(self):
        self._sensor.measure()
        return self._sensor.temperature(), self._sensor.humidity()
