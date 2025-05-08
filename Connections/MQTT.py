import time
import paho.mqtt.client as mqtt
import json

# MQTT Details
mqtt_server = "29149bc39a6c4a8890d51c27de41a970.s1.eu.hivemq.cloud"
mqtt_port = 8883
mqtt_user = "Sindhu"
mqtt_password = "Sindhu13"
topic = "weather/esp32"

# Initialize MQTT Client
client = mqtt.Client(client_id="PythonClient")
client.username_pw_set(mqtt_user, mqtt_password)

# Set up secure connection (SSL/TLS)
client.tls_set()

# Callback function for when the client connects
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code: {rc}")
    client.subscribe(topic)

# Callback function for when a message is received
def on_message(client, userdata, msg):
    print(f"Message received: {msg.payload.decode()}")

# Set the callbacks
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(mqtt_server, mqtt_port, 60)

# Start the loop
client.loop_start()

try:
    while True:
        # Allow the loop to process messages and maintain the connection
        time.sleep(1)

except KeyboardInterrupt:
    print("Disconnected from MQTT Broker")
    client.loop_stop()
    client.disconnect()
