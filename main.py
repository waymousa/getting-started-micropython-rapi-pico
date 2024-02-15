import os
import time
import ujson
import machine
import network
import uasyncio as asyncio
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

# Coroutine: blink on a timer
async def pollIoT():
    print("Task_pollIoT started")
    while True:
        print("Polling IoT core")
        try:
            print("Running check_msg")
            shaddowClient.check_msg()
        except:
            print("Task_pollIoT Exception: Unable to check for messages.")
        await asyncio.sleep_ms(1000)

async def updateIoT():
    print("Task_updateIoT started")
    while True:
        print("Task_updateIoT running")
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
        try:
            shaddowClient.publish(mesg)
        except:
            print("Task_updateIoT Exception: Unable to publish message.")
        await asyncio.sleep_ms(10000)

async def memrep():
    print("Task_memrep started")
    while True:
        print("Task_memrep running report")
        micropython.mem_info()
        await asyncio.sleep(20)
        
async def memclear():
    print("Task_memclear started")
    while True:
        print("Task_memclear running GC")
        gc.collect()
        gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
        await asyncio.sleep(25)
    
async def main():
    print("Task_main started")
    tasks = [asyncio.create_task(updateIoT()), \
             asyncio.create_task(pollIoT()), \
             asyncio.create_task(memrep()), \
             asyncio.create_task(memclear())]
    res = await asyncio.gather(*tasks, return_exceptions=True)

print("Lunching task scheduler")
asyncio.run(main())