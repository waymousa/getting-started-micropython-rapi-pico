import utime
from . import simple


class MQTTClient(simple.MQTTClient):
    DELAY = 2
    DEBUG = True

    def delay(self, i):
        utime.sleep(self.DELAY)

    def log(self, in_reconnect, e):
        if self.DEBUG:
            if in_reconnect:
                print("mqtt reconnect: %r" % e)
            else:
                print("mqtt: %r" % e)

    def reconnect(self):
        i = 0
        while 1:
            try:
                return super().connect(False)
            except OSError as e:
                self.log(True, e)
                i += 1
                self.delay(i)

    def publish(self, topic, msg, retain=False, qos=0):
        while 1:
            try:
                return super().publish(topic, msg, retain, qos)
            except OSError as e:
                self.log(False, e)
            self.reconnect()

    def wait_msg(self):
        #print("robust.wait_msg called")
        while 1:
            try:
                return super().wait_msg()
            except OSError as e:
                self.log(False, e)
            self.reconnect()

    def check_msg(self, attempts=2):
        #print("robust.check_msg called")
        while attempts:
            #print("calling setblocking")
            self.sock.setblocking(False)
            try:
                #print("calling super.wait_msg")
                return super().wait_msg()
            except OSError as e:
                self.log(False, e)
            except Exception as err:
                print(f"robust.check_msg Exception: Unexpected {err=}, {type(err)=}")
            print("calling reconnect")
            self.reconnect()
            attempts -= 1