import time
from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5050)
from counterfit_shims_grove.adc import ADC
from counterfit_shims_grove.grove_relay import GroveRelay
import paho.mqtt.client as mqtt
import json

# Sensor
adc = ADC()

# Actuator
relay = GroveRelay(5)

# MQTT Conecction
id = 'leo10923847leorier'
client_name = id + 'soilmoisturesensor_client'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org', 1883, 60)
mqtt_client.loop_start()
print("MQTT Connected!")

def handle_command(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)

    if payload['relay_on']:
        relay.on()
    else:
        relay.off()

mqtt_client.subscribe(server_command_topic)
mqtt_client.on_message = handle_command

while True:
    soil_moisture = adc.read(0)
    telemetry = json.dumps({'soil_moisture': soil_moisture})
    print("Sending telemetry:", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(10)
