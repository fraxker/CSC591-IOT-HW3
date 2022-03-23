import paho.mqtt.client as paho
import atexit
import time

class PI_C:
    def __init__(self):
        self.client_name = "RaspberryPiC"
        self.client = paho.Client(self.client_name)
        self.client.connect("mosquitto")
        self.client.on_message=self.on_message
        self.pi_status_topic = "Status/" + self.client_name
        self.client.will_set(self.pi_status_topic, payload="offine", retain=True, qos=2)
        self.client.loop_start()
        atexit.register(self.client.loop_stop)
        self.client.publish(self.pi_status_topic, "online", retain=True, qos=2)

        self.sensor_topic = "lightSensor"
        self.client.subscribe(self.sensor_topic, qos=2)

        self.threshold_topic = "threshold"
        self.client.subscribe(self.threshold_topic, qos=2)

        self.light_status_topic = "lightStatus"
        self.client.subscribe(self.light_status_topic, qos=2)
        self.status_payload = "TurnOff"
  
    def on_message(self, client, userdata, message):
        if message.topic == self.sensor_topic:
            self.light_payload = float(message.payload.decode("utf-8"))
            self.publish_command()
        elif message.topic == self.threshold_topic:
            self.threshold_payload = float(message.payload.decode("utf-8"))
            self.publish_command()
        elif message.topic == self.light_status_topic:
            self.status_payload = str(message.payload.decode("utf-8"))

    def publish_command(self):
        command = self.compare_sensors()
        if command is not self.status_payload:
            self.client.publish(self.light_status_topic, command, retain=True, qos=2)

    def compare_sensors(self):
        if self.light_payload >= self.threshold_payload:
            return "TurnOn"
        else:
            return "TurnOff"

if __name__ == "__main__":
    pi_c = PI_C()
    while True:
        time.sleep(1)
