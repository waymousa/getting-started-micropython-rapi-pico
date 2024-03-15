import os
import time
import ujson
import machine
import network
import asyncio
from umqtt.robust import MQTTClient
import utils.constants as constants
from mqttagent import MQTTAgent
from mqttagentfactory import MQTTAgentFactory
from wifihelper import WiFiHelper
from logging import logging
from router import Router
from shaddowupdater import ShaddowUpdater
from primitives.queue import Queue
from button import Button
from led import LED

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

#If you followed the blog, these names are already set.
client_id = constants.AWS_IOT_CLIENT_ID

#Define pins for LED and light sensor. In this example we are using a FeatherS2.
#The sensor and LED are built into the board, and no external connections are required.
led = machine.Pin("LED", machine.Pin.OUT)
info = os.uname()

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
    log.debug("Task_main started.")
    led = LED("LED")
    router = Router
    wifiHelper = WiFiHelper()
    await asyncio.sleep_ms(5000)
    shaddowClient = MQTTAgentFactory.create("main", router)
    shaddowUpdater = ShaddowUpdater(shaddowClient, led)
    button = Button(16,led)
    while True:
        await asyncio.sleep_ms(100)

log.info("Lunching task scheduler.")
asyncio.run(main())