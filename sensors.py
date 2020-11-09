import machine
import dht
import sgp30


class TempHumi:
    def __init__(self, out):
        self._sensor = dht.DHT11(out)

    def measure(self):
        self._sensor.measure()
        return self._sensor.temperature(), self._sensor.humidity()


class CO2TVOC:
    def __init__(self, scl, sda, freq=100000):
        i2c = machine.I2C(scl=scl, sda=sda, freq=freq)
        self._sensor = sgp30.Adafruit_SGP30(i2c)

    def measure(self):
        return self._sensor.iaq_measure()