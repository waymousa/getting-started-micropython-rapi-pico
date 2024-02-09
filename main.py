import os
import time
import ujson
import machine
import network
from umqtt.robust import MQTTClient
import utils.constants as constants
from utils.mqttclienthelper import MQTTClientHelper

#Enter your wifi SSID and password below.
wifi_ssid = constants.WIFI_SSID
wifi_password = constants.WIFI_PASSWORD

#Enter your AWS IoT endpoint. You can find it in the Settings page of
#your AWS IoT Core console. 
#https://docs.aws.amazon.com/iot/latest/developerguide/iot-connect-devices.html 
aws_endpoint = constants.AWS_IOT_CORE_HOST

#If you followed the blog, these names are already set.
thing_name = constants.AWS_IOT_THING_NAME
client_id = constants.AWS_IOT_CLIENT_ID
private_key = constants.AWS_IOT_DEVICE_KEY
private_cert = constants.AWS_IOT_DEVICE_CERT

#Read the files used to authenticate to AWS IoT Core
with open(private_key, 'rb') as f:
    key = f.read()
with open(private_cert, 'rb') as f:
    cert = f.read()

#These are the topics we will subscribe to. We will publish updates to /update.
#We will subscribe to the /update/delta topic to look for changes in the device shadow.
topic_pub = "$aws/things/" + thing_name + "/shadow/update"
topic_sub = "$aws/things/" + thing_name + "/shadow/update/delta"
ssl_params = {"key":key, "cert":cert, "server_side":False}

#Define pins for LED and light sensor. In this example we are using a FeatherS2.
#The sensor and LED are built into the board, and no external connections are required.
led = machine.Pin("LED", machine.Pin.OUT)
info = os.uname()

#Connect to the wireless network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('Connecting to network...')
    wlan.connect(wifi_ssid, wifi_password)
    while not wlan.isconnected():
        pass

    print('Connection successful')
    print('Network config:', wlan.ifconfig())

def mqtt_connect(client=client_id, endpoint=aws_endpoint, sslp=ssl_params):
    mqtt = MQTTClient(client_id=client, server=endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=sslp)
    print("Connecting to AWS IoT...")
    mqtt.connect()
    print("Done")
    return mqtt

def mqtt_publish(client, topic=topic_pub, message=''):
    print("Publishing message...")
    client.publish(topic, message)
    print(message)

def mqtt_subscribe(topic, msg):
    print("Message received...")
    message = ujson.loads(msg)
    print(topic, message)
    if message['state']['led']:
        led_state(message)
    print("Done")

def led_state(message):
    led.value(message['state']['led']['onboard'])

#We use our helper function to connect to AWS IoT Core.
#The callback function mqtt_subscribe is what will be called if we 
#get a new message on topic_sub.
'''
try:
    mqtt = mqtt_connect()
    mqtt.set_callback(mqtt_subscribe)
    mqtt.subscribe(topic_sub)
except:
    print("Unable to connect to MQTT.")
'''

shaddowClient = MQTTClientHelper(client_id=client_id, endpoint=aws_endpoint, sslp=ssl_params, pub_topic=topic_pub, sub_topic=topic_sub)
shaddowClient.connect()

while True:
#Check for messages.
    try:
        shaddowClient.check_msg()
        #mqtt.check_msg()
    except:
        print("Unable to check for messages.")

    mesg = ujson.dumps({
        "state":{
            "reported": {
                "device": {
                    "client": client_id,
                    "uptime": time.ticks_ms(),
                    "hardware": info[0],
                    "firmware": info[2]
                },
                "led": {
                    "onboard": led.value()
                }
            }
        }
    })

#Using the message above, the device shadow is updated.
    try:
        shaddowClient.publish(mesg)
        #mqtt_publish(client=mqtt, message=mesg)
    except:
        print("Unable to publish message.")

#Wait for 10 seconds before checking for messages and publishing a new update.
    print("Sleep for 10 seconds")
    time.sleep(10)