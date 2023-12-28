from paho.mqtt import client as mqtt_client
from dnull_mqtt.config import Config
import json
from dnull_mqtt.base_log import log


class MQTT:
    def __init__(self, Config: Config, topic) -> None:
        self.config = Config
        self.topic = f"{self.config.mtqq_prefix}/{topic}"
        self.client = self.connect()
        self.run()

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                log.info(f"Connected to MQTT Broker: {self.topic}")
            else:
                log.error(f"Failed to connect {self.topic}, return code %d\n", rc)

        client = mqtt_client.Client(f"python-mqtt-{self.topic}")
        client.username_pw_set(self.config.mqtt_username, self.config.mqtt_password)
        client.on_connect = on_connect
        client.connect(self.config.mqtt_broker, self.config.mqtt_port)
        return client

    def publish(self, msg):
        result = self.client.publish(self.topic, json.dumps(msg))
        status = result[0]
        if status == 0:
            log.info(f"{self.topic}: published")
            log.debug(f"{self.topic}: published {msg}")
        else:
            log.error(f"Failed to send message to topic {self.topic}")

    def run(self):
        self.client.loop_start()
