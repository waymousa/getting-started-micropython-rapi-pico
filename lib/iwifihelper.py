from abc.abc import abstractmethod

class IWifiHelper():
    "An abstract class to for the WifiHelper"
    
    @staticmethod
    @abstractmethod
    
    async def run():
        "An abstract async method."
        
    def join():
        "An abstract method."
        
    def isJoined():
        "An abstract method."
        
    def getIPAddress():
        "An abstract method."
        
    def getGWAddress():
        "An abstract method."
        
    def getDNS():
        "An abstract method."

    def getSubnetMask():
        "An abstract method."
        
    def getIfconfig():
        "An abstract method."