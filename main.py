import os
import time
import ujson
import machine
import network
from umqtt.simple import MQTTClient
import uasyncio
import utime
import queue
import micropython

#Enter your wifi SSID and password below.
wifi_ssid = "swaym-mobile-wifi"
wifi_password = "Piaggio!2"

#Enter your AWS IoT endpoint. You can find it in the Settings page of
#your AWS IoT Core console. 
#https://docs.aws.amazon.com/iot/latest/developerguide/iot-connect-devices.html 
#aws_endpoint = b'ah9frbb7pxug4-ats.iot.eu-west-1.amazonaws.com'
aws_endpoint = "ah9frbb7pxug4-ats.iot.eu-west-1.amazonaws.com"

#If you followed the blog, these names are already set.
thing_name = "RaPi-Pico-2040"
client_id = "RaPi-Pico-2040-Client"
private_key = "cert/private.key.der"
private_cert = "cert/certificate.crt.der"

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
#light_sensor = machine.ADC(machine.Pin(4))
#light_sensor.atten(machine.ADC.ATTN_11DB)
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
    print('client_id:', client)
    print('server:', endpoint)
    print('ssl_params:', sslp)
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
try:
    mqtt = mqtt_connect()
    mqtt.set_callback(mqtt_subscribe)
    mqtt.subscribe(topic_sub)
except Exception as err:
    print(f"Unexpected {err=}, {type(err)=}")
#except:
#    print("Unable to connect to MQTT.")

# Coroutine: blink on a timer
async def pollIoT():
    print("Starting pollIoT")
    while True:
        #print("Polling IoT core")
        try:
            mqtt.check_msg()
        except:
            print("Unable to check for messages.")
        await uasyncio.sleep_ms(1000)
        
async def updateIoT():
    print("Starting updateIoT")
    while True:
        mesg = ujson.dumps({
        "state":{
            "reported": {
                "device": {
                    "client": client_id,
                    "uptime": time.ticks_ms(),
                    "hardware": info[0],
                    "firmware": info[2]
                },
                #"sensors": {
                #    "light": light_sensor.read()
                #},
                "led": {
                    "onboard": led.value()
                }
            }
        }
    })
        try:
            mqtt_publish(client=mqtt, message=mesg)
        except:
            print("Unable to publish message.")
        await uasyncio.sleep_ms(10000)
        
async def memrep():
    print("Starting memrep")
    while True:
        micropython.mem_info()
        await uasyncio.sleep(20)
        
async def memclear():
    print("Starting memclear")
    while True:
        print("Running GC")
        gc.collect()
        gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
        await uasyncio.sleep(25)
        
async def main():
    print("Running the main coroutine")
    tasks = [uasyncio.create_task(updateIoT()),uasyncio.create_task(pollIoT()),uasyncio.create_task(memrep()),uasyncio.create_task(memclear())]
    res = await uasyncio.gather(*tasks, return_exceptions=True)
    #updateTask = uasyncio.create_task(updateIoT())
    #pollTask = uasyncio.create_task(pollIoT())
    #await uasyncio.sleep_ms(20000)

print("Starting task loop")
uasyncio.run(main())

'''while True:
#Check for messages.
    try:
        mqtt.check_msg()
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
                #"sensors": {
                #    "light": light_sensor.read()
                #},
                "led": {
                    "onboard": led.value()
                }
            }
        }
    })

#Using the message above, the device shadow is updated.
    try:
        mqtt_publish(client=mqtt, message=mesg)
    except:
        print("Unable to publish message.")

#Wait for 10 seconds before checking for messages and publishing a new update.
    print("Sleep for 10 seconds")
    time.sleep(10)'''