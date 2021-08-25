import paho.mqtt.client as mqtt

from send import send_cmd

SERVER_IP = '83.150.204.55'
SERVER_PORT = 40883
CLIENT_ID = 'testclient_rpi'

SELF_NAME = 'RPI_TEST_DEVICE_1'
MQTT_TOPIC = 'test'

###################
# TODO: add other possible commands
OPEN_COMMAND = 'OPEN'
###################

def on_connect(client, userdata, flags, rc):
    client.publish(MQTT_TOPIC, SELF_NAME)
    client.subscribe(MQTT_TOPIC)
    print('connected')

def on_disconnect(client, userdata, rc):
    print("Disconnect, reason: " + str(rc))
    print("Disconnect, reason: " + str(client))

def on_message(client, userdata, msg):
    if msg.payload.decode("utf-8") == OPEN_COMMAND:
        # TODO: remove strip/lower
        send_cmd(OPEN_COMMAND.strip().lower())
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client(CLIENT_ID, protocol=mqtt.MQTTv31)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.connect(SERVER_IP, SERVER_PORT, keepalive=60)
client.loop_forever()

