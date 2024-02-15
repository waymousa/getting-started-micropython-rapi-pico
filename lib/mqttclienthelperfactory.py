from mqttclienthelper import MQTTClientHelper
import utils.constants as constants
from umqtt.robust import MQTTClient

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

class MQTTClientHelperFactory:
    
    @staticmethod
    def create(client_to_create):
        "A static method to create a new MQTT Client Helper"
        if client_to_create == 'main':
            print("MQTTClientHelperFactory.create(main)")
            topic_pub = "$aws/things/" + thing_name + "/shadow/update"
            topic_sub = "$aws/things/" + thing_name + "/shadow/update/delta"
            mqtt = MQTTClientHelper(client_id=client_id, \
                              endpoint=aws_endpoint, \
                              pub_topic = topic_pub, \
                              sub_topic = topic_sub, \
                              sslp=ssl_params)
            #mqtt.connect()
            return mqtt
        
        return None
    
    
    