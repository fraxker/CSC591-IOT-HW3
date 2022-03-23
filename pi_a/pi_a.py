import paho.mqtt.client as paho
import time
import atexit
import serial
from gpiozero import LightSensor

class PI_A:
    def __init__(self):
        self.arduino = serial.Serial(port='ttyACM0', baudrate=115200, timeout=.1)
        self.ldr = LightSensor(18)

        self.offline_str = "offline"
        self.online_str = "online"
        self.turn_off_str = "TurnOff"
        self.turn_on_str = "TurnOn"

        self.client_name = "RaspberryPiA"
        self.client = paho.Client(self.client_name)
        self.client.connect("192.168.1.101")
        self.client.on_message=self.on_message
        self.pi_status_topic = "Status/" + self.client_name
        self.client.will_set(self.pi_status_topic, payload=self.offline_str, retain=True, qos=2)

        self.sensor_topic = "lightSensor"
        self.client.subscribe(self.sensor_topic, qos=2)
        self.threshold_topic = "threshold"
        self.client.subscibe(self.threshold_topic, qos=2)

        self.client.loop_start()
        atexit.register(self.client.loop_stop)
        self.client.publish(self.pi_status_topic, self.online_str, retain=True, qos=2)

    def on_message(self, client, userdata, message):
        command = str(message.payload.decode("utf-8"))
        if message.topic is self.sensor_topic:
            self.old_ldr = float(command)
        elif message.topic is self.threshold_topic:
            self.old_pot = float(command)
        else:
            raise Exception("Unreconized topic: " + message.topic)
    
    def run_loop(self):
        light = self.ldr.value
        print(light)
        if light != self.old_ldr:
            self.client.publish(self.sensor_topic, str(light), retain=True, qos=2)
        pot = float(self.arduino.readline())
        print(pot)
        if pot != self.old_pot:
            self.client.publish(self.threshold_topic, str(pot), retain=True, qos=2)

if __name__ == "__main__":
    pi_a = PI_A()
    while True:
        pi_a.run_loop()
        time.sleep(.1)