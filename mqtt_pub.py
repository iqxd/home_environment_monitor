import json
from simple import MQTTClient


class MQTT_CLI:
    def __init__(self, wl, name, server):
        self._cli = MQTTClient(name, server)
        if not wl.isconnected():
            wl.connect()
        self._cli.connect()
        self._cli.disconnect()

    def publish(self, topic, msgobj):
        try:
            self._cli.connect()
            msgstr = json.dumps(msgobj)
            self._cli.publish(topic.encode(), msgstr.encode())
            self._cli.disconnect()
        except:
            pass
