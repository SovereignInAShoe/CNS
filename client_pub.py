import paho.mqtt.client as mqtt
import time
import json
from Crypto.Cipher import AES

def pad_message(message):
    while len(message) % 16 != 0:
        message = message + " "
    return message

C_TOPIC_EXCHANGE = 'topics_exchange'

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

TOPICS = [
    'living_room/bulb1/status'
]

ENC_TOPICS = [Obfs(t).hex() for t in TOPICS]

###

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    #client.subscribe("$SYS/#")
    client.publish(C_TOPIC_EXCHANGE, json.dumps(ENC_TOPICS))

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


def on_publish(client, userdata, result):
    print("data published", result, '\n')
    pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

client.connect("127.0.0.1", 1883, 60)

client.publish(C_TOPIC_EXCHANGE, json.dumps(ENC_TOPICS))

while True:
    print(ENC_TOPICS[0], 'on')
    ret = client.publish(ENC_TOPICS[0], "on") # TODO should use some wrap functions, being lazy here
    time.sleep(3)
