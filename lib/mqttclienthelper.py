from umqtt.robust import MQTTClient
import utils.constants as constants
from led import led
import ujson
from imqttclienthelper import IMQTTClientHelper

class MQTTClientHelper(IMQTTClientHelper):
    
    def __init__(self, client_id, endpoint, sslp, pub_topic, sub_topic):
        self.client_id = client_id
        self.endpoint = endpoint
        self.sslp = sslp
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic
        self.led = led("LED")
        self.mqtt = None
        
    def connect(self):
        self.mqtt = MQTTClient(client_id=self.client_id, server=self.endpoint, port=8883, keepalive=1200, ssl=True, ssl_params=self.sslp)
        print("Connecting to AWS IoT...")
        self.mqtt.connect()
        self.mqtt.set_callback(self.subscribe)
        self.mqtt.subscribe(self.sub_topic)
        print("Done")
        return self.mqtt
    
    def publish(self, message=''):
        print("Publishing message...")
        self.mqtt.publish(self.pub_topic, message)
        print(message)
        
    def subscribe(self, topic, msg):
        print("Receiving message...")
        message = ujson.loads(msg)
        print(topic, message)
        if message['state']['led']:
            #print("mqttclienthelper.subscribe setting led")
            self.led.led_state(message)
        print("Done")
    
    def check_msg(self):
        #print("mqttclienthelper.check_msg called")
        try:
            self.mqtt.check_msg()
        except Exception as err:
            print(f"check_msg Exception: Unexpected {err=}, {type(err)=}")
        