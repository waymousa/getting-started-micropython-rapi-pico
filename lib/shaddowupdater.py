# Updates the remote shaddow with the latest state of the device
import utils.constants as constants
from logging import logging
import time
import ujson
from led import LED
import os
import asyncio
import machine

log = logging.getLogger(__name__)

client_id = constants.AWS_IOT_CLIENT_ID

#led = machine.Pin("LED", machine.Pin.OUT)
info = os.uname()

class ShaddowUpdater:
    
    def __init__(self, client, led):
        log.debug('ShaddowUpdater created')
        self.client = client
        self.message = ""
        self.led = led
        log.debug('Starting task...')
        self.task = asyncio.create_task(self.run())
        
    async def run(self):
        log.debug('run started...')
        while True:
            log.debug('Running...')
            self.update()
            await asyncio.sleep_ms(constants.SHADDOW_UPDATE_RATE_MS)
            
    def update(self):
        log.debug('Update running...')
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
                        "onboard": self.led.led_value()
                    }
                }
            }
        })
        log.debug(mesg)
        try:
            log.debug('Client publishing...')
            self.client.publish(mesg)
        except:
            log.error("Task_updateIoT Exception: Unable to publish message.")
        