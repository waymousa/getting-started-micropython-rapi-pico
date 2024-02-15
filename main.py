import os
import time
import ujson
import machine
import network
from umqtt.robust import MQTTClient
import utils.constants as constants
from mqttclienthelper import MQTTClientHelper
from mqttclienthelperfactory import MQTTClientHelperFactory

#Enter your wifi SSID and password below.
wifi_ssid = constants.WIFI_SSID
wifi_password = constants.WIFI_PASSWORD

#If you followed the blog, these names are already set.
client_id = constants.AWS_IOT_CLIENT_ID

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

shaddowClient = MQTTClientHelperFactory.create("main")
shaddowClient.connect()

while True:
#Check for messages.
    try:
        shaddowClient.check_msg()
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
    except:
        print("Unable to publish message.")

#Wait for 10 seconds before checking for messages and publishing a new update.
    print("Sleep for 10 seconds")
    time.sleep(10)