import paho.mqtt.client as mqtt

import time
import json
from Crypto.Cipher import AES

def pad_message(message):
    while len(message) % 16 != 0:
        message = message + " "
    return message

C_TOPIC_EXCHANGE = 'topics_exchange'


EXCHANGED_TOPICS = {}

SECRET = 'demoopurposessss'.encode('utf-8')

def Enc(t):
    cipher = AES.new(SECRET, AES.MODE_ECB)
    t = pad_message(t)
    return cipher.encrypt(t.encode('utf-8'))

def Dec(t):
    decipher = AES.new(SECRET, AES.MODE_ECB)
    return decipher.decrypt(t).decode('utf-8')

def Obfs(t):
    return Enc(t)

def DeObfs(t):
    return Dec(t)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(C_TOPIC_EXCHANGE)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == C_TOPIC_EXCHANGE:
        enc_topics = json.loads(msg.payload)
        # keep refresh the topics
        global EXCHANGED_TOPICS
        EXCHANGED_TOPICS = {t : str(DeObfs(bytes.fromhex(t))).strip() for t in enc_topics}
        print('EXCHANGED_TOPICS', EXCHANGED_TOPICS)
        for t in enc_topics:
            client.subscribe(t)

    # user definiton emulation
    elif EXCHANGED_TOPICS[msg.topic] == 'living_room/bulb1/status':
        print(msg.payload, EXCHANGED_TOPICS[msg.topic],)

        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("127.0.0.1", 1883, 60)

client.subscribe(C_TOPIC_EXCHANGE)
# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
