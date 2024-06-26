from abc.abc import abstractmethod

class IMQTTClientAgent():
    "An abstract class to for the MQTTClientHelper"
    
    @staticmethod
    @abstractmethod
    
    def connect():
        "An abstract method."
        
    def publish(self, message=''):
        "An abstract method."
        
    def subscribe(self, topic, msg):
        "An abstract method."
        
    def check_msg(self):
        "An abstract method."