import paho.mqtt.client as paho
import time
import atexit
from gpiozero import LED

class PI_B:
    def __init__(self):

        self.led1 = LED(14)
        self.led2 = LED(15)
        self.led3 = LED(18)
        self.led1.off()
        self.led2.off()
        self.led3.off()

        self.offline_str = "offline"
        self.online_str = "online"
        self.turn_off_str = "TurnOff"
        self.turn_on_str = "TurnOn"

        self.client_name = "RaspberryPiB"
        self.client = paho.Client(self.client_name)
        self.client.connect("192.168.1.101")
        self.client.on_message=self.on_message
        self.client.loop_start()
        atexit.register(self.client.loop_stop)

        self.pia_topic = "Status/RaspberryPiA"
        self.pic_topic = "Status/RaspberryPiC"
        self.light_topic = "lightStatus"
        self.client.subscribe(self.pia_topic, qos=2)
        self.client.subscribe(self.pic_topic, qos=2)
        self.client.subscribe(self.light_topic, qos=2)


    def on_message(self, client, userdata, message):
        command = str(message.payload.decode("utf-8"))
        if message.topic == self.pia_topic:
            if command == self.online_str:
                self.led2.on()
            elif command == self.offline_str:
                self.led2.off()
            else:
                raise Exception("Invalid command from rpi a: "+ command)
        elif message.topic == self.pic_topic:
            if command == self.online_str:
                self.led3.on()
            elif command == self.offline_str:
                self.led3.off()
            else:
                raise Exception("Invalid command from rpi c: "+ command)
        elif message.topic == self.light_topic:
            if command == self.turn_on_str:
                self.led1.on()
            elif command == self.turn_off_str:
                self.led1.off()
            else:
                raise Exception("Invalid command from light status: "+ command)
        else:
            raise Exception("Unreconized topic: " + message.topic)

if __name__ == "__main__":
    pi_b = PI_B()
    while True:
        time.sleep(1)