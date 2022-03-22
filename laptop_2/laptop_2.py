import paho.mqtt.client as paho
from datetime import datetime
import time

def on_message(client, userdata, message):
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print(message.topic, ": ", str(message.payload.decode("utf-8")), current_time)

if __name__ == "__main__":
    client = paho.Client("Laptop 2")
    client.connect("mosquitto")
    client.on_message=on_message
    client.subscribe("lightSensor", qos=2)
    client.subscribe("threshold", qos=2)
    client.subscribe("LightStatus", qos=2)
    client.subscribe("Status/RaspberryPiA", qos=2)
    client.subscribe("Status/RaspberryPiC", qos=2)

    client.loop_start()
    while True:
        time.sleep(1)