import time
from counterfit_connection import CounterFitConnection
from counterfit_shims_seeed_python_dht import DHT
import paho.mqtt.client as mqtt
import json

CounterFitConnection.init('127.0.0.1', 5050)

sensor = DHT("11", 5)

# MQTT connection
id = 'leo10923847leorier'
client_name = id + 'temperature_sensor_client'
client_telemetry_topic = id + '/telemetry'
#server_command_topic = id + '/commands'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org', 1883, 60)
mqtt_client.loop_start()
print("MQTT connected!")

while True:
    _, temp = sensor.read()
    telemetry = json.dumps({'temperature' : temp})
    print("Sending telemetry ", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)


