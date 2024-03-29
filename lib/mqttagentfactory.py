from mqttagent import MQTTAgent
import utils.constants as constants
from umqtt.robust import MQTTClient
from logging import logging

log = logging.getLogger(__name__)

aws_endpoint = constants.AWS_IOT_CORE_HOST
thing_name = constants.AWS_IOT_THING_NAME
client_id = constants.AWS_IOT_CLIENT_ID
private_key = constants.AWS_IOT_DEVICE_KEY
private_cert = constants.AWS_IOT_DEVICE_CERT

with open(private_key, 'rb') as f:
    key = f.read()
with open(private_cert, 'rb') as f:
    cert = f.read()    

ssl_params = {"key":key, "cert":cert, "server_side":False}

class MQTTAgentFactory:
    
    @staticmethod
    def create(client_to_create, router):
        "A static method to create a new MQTTAgent"
        if client_to_create == 'main':
            log.debug("Creating MQTTAgent")
            topic_pub = "$aws/things/" + thing_name + "/shadow/update"
            topic_sub = "$aws/things/" + thing_name + "/shadow/update/delta"
            mqtt = MQTTAgent(client_id=client_id, \
                              endpoint=aws_endpoint, \
                              pub_topic = topic_pub, \
                              sub_topic = topic_sub, \
                              sslp=ssl_params,
                              router=router)
            return mqtt
        
        return None
    
    
    