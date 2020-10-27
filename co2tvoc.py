import machine
import sgp30


class CO2TVOC:
    def __init__(self, scl, sda, freq=100000):
        i2c = machine.I2C(scl=scl, sda=sda, freq=freq)
        self._sensor = sgp30.Adafruit_SGP30(i2c)

    def measure(self):
        return self._sensor.iaq_measure()
