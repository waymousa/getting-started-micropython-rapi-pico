from iwifihelper import IWifiHelper
import utils.constants as constants
import network
import uasyncio as asyncio
from logging import logging

log = logging.getLogger(__name__)

class WiFiHelper(IWifiHelper):
    
    def __init__(self):
        log.debug('WiFiHelper created.')
        self.wifi_ssid = constants.WIFI_SSID
        self.wifi_password = constants.WIFI_PASSWORD
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        log.debug('Starting task...')
        self.task = asyncio.create_task(self.run())
    
    async def run(self):
        log.debug('WiFiHelper.run started...')
        while True:
            self.join()
            await asyncio.sleep_ms(constants.WIFI_RECHECK_RATE_MS)
        
    def join(self):
        log.debug('WiFiHelper.join started...')
        if not self.wlan.isconnected():
            log.info('Connecting WiFi...')
            self.wlan.connect(self.wifi_ssid, self.wifi_password)
            while not self.wlan.isconnected():
                pass
            log.info('Connection successful.')
            self.getIfconfig()
        log.info('WiFi connected.')
    
    def getIPAddress(self):
        print('IP Address: ', self.wlan.ifconfig(0))
        
    def getGWAddress(self):
        print('GW Address: ', self.wlan.ifconfig(2))
        
    def getDNS(self):
        print('DNS Server: ', self.wlan.ifconfig(3))

    def getSubnetMask(self):
        print('Subnet mask: ', self.wlan.ifconfig(1))
        
    def getIfconfig(self):
        print('Network Config: ', self.wlan.ifconfig())