import network
import time


class Wireless:
    def __init__(self, wifiname, password):
        self._wlan = self._activate()
        self._wifiname = wifiname
        self._password = password

    def _activate(self):
        ap = network.WLAN(network.AP_IF)
        if ap.active():
            ap.active(False)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        assert wlan.active()
        return wlan

    def connect(self):
        self._wlan.connect(self._wifiname, self._password)
        for i in range(15):
            if self._wlan.isconnected():
                return True
            time.sleep(1)
        else:
            return False

    def isconnected(self):
        return self._wlan.isconnected()
