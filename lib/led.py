import machine
from logging import logging

log = logging.getLogger(__name__)

class LED():
    
    def __init__(self, pin):
        log.debug("led created.")
        self.led = machine.Pin(pin, machine.Pin.OUT)
        
    def led_state(self, message):
        log.debug("led.led_state called")
        self.led.value(message['state']['led']['onboard'])
        
    def toggle(self):
        log.debug("led.toggle called")
        log.debug(self.led.value())
        if self.led.value():
            log.debug("Setting led value to 0.")
            self.led.value(0)
        else:
            log.debug("Setting led value to 1.")
            self.led.value(1)
    
    def led_value(self):
        log.debug("led_value called")
        return self.led.value()
    