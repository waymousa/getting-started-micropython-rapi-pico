from abc.abc import abstractmethod

class IMQTTClientAgent():
    """An abstract class to for the MQTTClientAgent"""
    
    @abstractmethod
    def run(self):
        """The run method sets up the object with a task that will check the MQTT topic for
        messages and publish the current state of the device from memory as a json document to a topic."""
    
    @abstractmethod
    def connect():
        """This method runs the connects the agent to the MQTT endpoint."""
        
    @abstractmethod
    def publish(self, message=''):
        """This method accepts a message and published the message to the MQTT endpoint."""

    @abstractmethod
    def subscribe(self, topic, msg):
        """This method subscribes to an MQTT endpoint and particular topics."""

    @abstractmethod
    def check_msg(self):
        """This method checks for new messages."""