import machine
from logging import logging

log = logging.getLogger(__name__)

class led():
    
    def __init__(self, pin):
        self.led = machine.Pin(pin, machine.Pin.OUT)
        
    def led_state(self, message):
        log.debug("led.led_state called")
        self.led.value(message['state']['led']['onboard'])
    