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
        self.speed = 0
        self.brake = 0
        self.lane_change = 0
        self.client_id = client_id
        
    def set_state(self, message):
        log.debug("Setting car state.")
        log.debug(message)
        
        log.debug("Checking to see if there is a led item in the dict...")
        
        """
        Test message for iot core using and led change
        {
            "state": {
                "desired": {
                    "led": {
                         "onboard" : 1
                     }
                   }
             }
        }
        """        
        
        try:
            if message['state']['led']:
                log.debug("Setting car LED state")
                self.led.led_state(message['state']['led']['onboard'])
                log.debug("LED state is %s ", self.led.led_getstate())
        except:
            log.debug("No led item in the dict.")
        
        log.debug("Checking to see if there is a speed item in the dict...")
        
        """
        Test message for iot core using a speed change
        {
        "state": {
            "desired": {
                "speed": 1
                }
            }
        }
        """
        
        try:
            if message['state']['speed'] >= 0:
                log.debug("Setting car speed")
                self.speed = message['state']['speed']
                log.debug("Car speed is %s ", self.speed)
        except:
            log.debug("No speed item in the dict.")
            
        log.debug("Checking to see if there is a brake item in the dict...")
        
        """
        Test message for iot core using a speed change
        {
        "state": {
            "desired": {
                "brake": 1
                }
            }
        }
        """
        
        try:
            if message['state']['brake'] >= 0:
                log.debug("Setting car brake")
                self.brake = message['state']['brake']
                log.debug("Car brake is %s ", self.brake)
        except:
            log.debug("No brake item in the dict.")
            
        log.debug("Checking to see if there is a lane_change item in the dict...")
        
        """
        Test message for iot core using a lane_change change
        {
        "state": {
            "desired": {
                "lane_change": 1
                }
            }
        }
        """
        
        try:
            if message['state']['lane_change'] >= 0:
                log.debug("Setting car lane_change")
                self.lane_change = message['state']['lane_change']
                log.debug("Car brake is %s ", self.lane_change)
        except:
            log.debug("No lane_change item in the dict.")
                   
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
                },
                "speed": self.speed,
                "brake": self.brake,
                "lane_change": self.lane_change
            }
        }
        })
        
        log.debug("Returning car state: ")
        log.debug(message)
        
        return message
 