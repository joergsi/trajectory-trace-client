import paho.mqtt.client as mqtt
import json

class MQTTClient:

    def __init__(self, config, qos=1, connect_timeout=10):
        self.host = config['HOST']
        self.port = config['PORT']
        self.topic = f"{config['TOPIC']}/{config['SENSORNAME']}"
        self.transport = config['TRANSPORT']
        self.qos = qos
        self.connected = False
        self.client = mqtt.Client(transport=self.transport)
        if self.transport == "websockets":
            self.client.ws_set_options(path="/mqtt")
            self.client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
        self.client.username_pw_set(config['USER'], config['PW'])
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()
        # Wait for connection
        import time
        start = time.time()
        while not self.connected:
            if time.time() - start > connect_timeout:
                raise TimeoutError("MQTT connection timeout")
            time.sleep(0.1)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
        else:
            print(f"MQTT connect failed with code {rc}")

    def _on_disconnect(self, client, userdata, rc):
        self.connected = False

    def publish(self, payload):
        # Wait for connection if needed
        if not self.connected:
            print("[MQTT] Not connected, waiting...")
            import time
            start = time.time()
            while not self.connected:
                if time.time() - start > 10:
                    raise TimeoutError("MQTT connection timeout during publish")
                time.sleep(0.1)
        # Publish with QoS
        result = self.client.publish(self.topic, json.dumps(payload, indent=2), qos=self.qos)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"[MQTT] Publish failed: {result.rc}")

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
