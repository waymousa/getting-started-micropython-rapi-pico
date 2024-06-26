from logging import logging
from led import led
import ujson
import os
import time

log = logging.getLogger(__name__)

class CarStateManager():
    
    def __init__(self, client_id):
        log.debug("CarStateManager init.")
        self.led = led("LED")
        self.client_id = client_id
        
    def set_state(self, message):
        log.debug("Setting car state.")
        if message['state']['led']:
            log.debug("Setting car LED state")
            self.led.led_state(message)
        
    def get_state(self):
        log.debug("Getting car state")
        info = os.uname()
        message = ujson.dumps({
        "state":{
            "reported": {
                "device": {
                    "client": self.client_id,
                    "uptime": time.ticks_ms(),
                    "hardware": info[0],
                    "firmware": info[2]
                },
                "led": {
                    "onboard": self.led.led_getstate()
                }
            }
        }
        })
        
        return message
 