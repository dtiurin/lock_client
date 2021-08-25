import paho.mqtt.client as mqtt

from send import send_cmd


class MQTTConnectionManager(mqtt.Client):
    PROTOCOL = mqtt.MQTTv31
    SERVER_IP = '83.150.204.55'
    SERVER_PORT = 40883
    
    # NOTE: unique per device data
    CLIENT_ID = 'testclient_rpi'
    DEVICE_NAME = 'RPI_TEST_DEVICE_1'
    MQTT_TOPIC = 'test'

    def __init__(self,):
        # TODO: move commands to some device class
        self.OPEN_COMMAND = 'OPEN'

        super().__init__(self.CLIENT_ID, self.PROTOCOL)
        self.establish_connection()

    def establish_connection(self):
        self.connect(self.SERVER_IP, self.SERVER_PORT, keepalive=60)
        self.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        client.publish(self.MQTT_TOPIC, self.DEVICE_NAME)
        client.subscribe(self.MQTT_TOPIC)
        # TODO: check if web-server available (ping-request)
        # TODO: if server available make discovery (send amount of locks)
        print('MQTT connection established, discovery process finished.')

    def on_disconnect(self, client, userdata, rc):
        print(f'Disconnect, reason: {rc}')
        # TODO: add re-connect mechanism

    def on_message(self, client, userdata, msg):
        if msg.payload.decode("utf-8") == self.OPEN_COMMAND:
            # TODO: remove strip/lower
            send_cmd(self.OPEN_COMMAND.strip().lower())
        # TODO: add another commands handlers

        print(f'TOPIC: {msg.topic}; COMMAND: {msg.payload}')

if __name__ == '__main__':
    MQTTConnectionManager()
