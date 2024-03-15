from machine import Pin
from logging import logging
import asyncio
from led import LED

log = logging.getLogger(__name__)

class Button():
    
    def __init__(self, pin, led):
        self.led = led
        self.button = Pin(pin, Pin.IN, Pin.PULL_DOWN)
        self.task = asyncio.create_task(self.run())
    
    async def run(self):
        log.debug('Button.run started.')
        while True:
            if self.button.value():
                log.debug("Button pressed.")
                log.debug(self.button.value())
                self.led.toggle()
            await asyncio.sleep_ms(500)