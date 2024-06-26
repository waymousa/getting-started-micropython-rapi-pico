from umqtt.robust import MQTTClient
import utils.constants as constants
from led import led
import ujson
from imqttclientagent import IMQTTClientAgent
from logging import logging
import uasyncio as asyncio
from carstate import CarStateManager

log = logging.getLogger(__name__)

class MQTTClientAgent(IMQTTClientAgent):
    
    def __init__(self, client_id, endpoint, sslp, pub_topic, sub_topic, agent_id, observer):
        self.client_id = client_id
        self.endpoint = endpoint
        self.sslp = sslp
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic
        self.agent_id = agent_id
        self.observer = observer
        self.mqtt = MQTTClient(client_id=self.client_id, server=self.endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=self.sslp)
        self.connect()
        log.debug('Starting task...')
        self.task = asyncio.create_task(self.run())
        
    async def run(self):
        log.debug('%s MQTTClientAgent.run started...', self.agent_id)
        while True:
            self.check_msg()
            await asyncio.sleep_ms(constants.AWS_IOT_MQTT_RECHECK_RATE_MS)
            self.publish()
            await asyncio.sleep_ms(constants.AWS_IOT_MQTT_RECHECK_RATE_MS)
        
    def connect(self):        
        log.info("%s MQTTClientAgent Connecting to AWS IoT...", self.agent_id)
        self.mqtt.connect()
        self.mqtt.set_callback(self.subscribe)
        self.mqtt.subscribe(self.sub_topic)
        log.info("Done")
        return self.mqtt
    
    def publish(self, message=''):
        log.info("%s MQTTClientAgent publishing message...", self.agent_id)
        
        message = self.observer.get_state()
            
        try:
            self.mqtt.publish(self.pub_topic, message)
        except:
            print("%s MQTTClientAgent Exception: Unable to publish message.", self.agent_id)
        log.info(message)
        
    def subscribe(self, topic, msg):
        log.info("%s MQTTClientAgent receiving message...", self.agent_id)
        message = ujson.loads(msg)
        log.info(topic, message)
        self.observer.set_state(message)
        log.debug("%s MQTTClientAgent message done.", self.agent_id)
    
    def check_msg(self):
        log.info("%s MQTTClientAgent Checking for messages.", self.agent_id)
        try:
            self.mqtt.check_msg()
        except Exception as err:
            log.error(f"check_msg Exception: Unexpected {err=}, {type(err)=}")
        
