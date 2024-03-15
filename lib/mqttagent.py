from umqtt.robust import MQTTClient
import utils.constants as constants
from led import LED
import ujson
from imqttagent import IMQTTAgent
from logging import logging
import asyncio
from router import Router
from primitives.queue import Queue

log = logging.getLogger(__name__)

class MQTTAgent(IMQTTAgent):
    
    def __init__(self, client_id, endpoint, sslp, pub_topic, sub_topic, router):
        self.client_id = client_id
        self.endpoint = endpoint
        self.sslp = sslp
        self.pub_topic = pub_topic
        log.debug(self.pub_topic)
        self.sub_topic = sub_topic
        log.debug(self.sub_topic)
        self.led = LED("LED")
        self.router = router
        self.mqtt = MQTTClient(client_id=self.client_id, server=self.endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=self.sslp)
        self.connect()
        log.debug('Starting task...')
        self.task = asyncio.create_task(self.run())
        
    async def run(self):
        log.debug('MQTTAgent.run started...')
        while True:
            self.check_msg()
            await asyncio.sleep_ms(constants.AWS_IOT_MQTT_RECHECK_RATE_MS)
        
    def connect(self):        
        log.info("Connecting to AWS IoT...")
        self.mqtt.connect()
        self.mqtt.set_callback(self.subscribe)
        self.mqtt.subscribe(self.sub_topic)        
        log.info("Done")
        return self.mqtt
    
    def publish(self, message=''):
        log.info("Publishing message...")
        self.mqtt.publish(self.pub_topic, message)
        log.info(message)
        
    def subscribe(self, topic, msg):
        log.info("Receiving message...")
        message = ujson.loads(msg)
        log.debug('Sending message to queue')
        result = message['state']['led']['onboard']
        log.debug(result)
        await self.router.put(result)
        if message['state']['led']:
            print("mqttagent.subscribe setting led")
            self.led.led_state(message)
        log.info("Done")
    
    def check_msg(self):
        log.info("Checking for messages.")
        try:
            self.mqtt.check_msg()
        except Exception as err:
            log.error(f"check_msg Exception: Unexpected {err=}, {type(err)=}")
        
