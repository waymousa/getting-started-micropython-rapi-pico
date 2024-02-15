import machine

class led():
    
    def __init__(self, pin):
        self.led = machine.Pin(pin, machine.Pin.OUT)
        
    def led_state(self, message):
        #print("led.led_state called")
        self.led.value(message['state']['led']['onboard'])
    