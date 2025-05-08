from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import ssl
import logging
import time
import json

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# MQTT (HiveMQ Cloud) details
MQTT_BROKER = "29149bc39a6c4a8890d51c27de41a970.s1.eu.hivemq.cloud"
MQTT_PORT = 8883
MQTT_TOPIC = "weather/esp32"
MQTT_USERNAME = "Sindhu"
MQTT_PASSWORD = "Sindhu13"

# InfluxDB 2.x connection details
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "K3yC8zERcrnJ0G7hEh_26caVuFA7xwhUzyEExy--cz2AUThswdPeMmubXc8E0XzzSRl9vWs4Sqze7JFN1UUFSw=="
INFLUX_ORG = "rowan"
INFLUX_BUCKET = "mybucket"

# Verify InfluxDB connection first
try:
    client_influx = InfluxDBClient(
        url=INFLUX_URL,
        token=INFLUX_TOKEN,
        org=INFLUX_ORG,
        timeout=10000
    )
    health = client_influx.health()
    logger.info(f"InfluxDB connection: {health.status}")
    
    # Get bucket info to verify bucket exists
    buckets_api = client_influx.buckets_api()
    buckets = buckets_api.find_buckets().buckets
    bucket_names = [bucket.name for bucket in buckets]
    logger.info(f"Available buckets: {bucket_names}")
    
    if INFLUX_BUCKET not in bucket_names:
        logger.error(f"Bucket '{INFLUX_BUCKET}' not found!")
        
    write_api = client_influx.write_api(write_options=SYNCHRONOUS)
except Exception as e:
    logger.error(f"Failed to connect to InfluxDB: {str(e)}")
    exit(1)

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to HiveMQ Cloud")
        client.subscribe(MQTT_TOPIC)
    else:
        logger.error(f"Failed to connect to HiveMQ. Code: {rc}")

def on_message(client, userdata, msg):
    logger.info("MQTT on_message triggered!")
    try:
        # Parse the incoming message (assuming JSON format)
        data = json.loads(msg.payload.decode())
        
        # Extract data from the message
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        pressure = data.get("pressure")
        location = data.get("location")  # Assuming location is part of the message
        altitude = data.get("altitude")  # Assuming altitude is part of the message

        # Log the extracted data for verification
        logger.debug(f"Extracted - Temperature: {temperature}, Humidity: {humidity}, Pressure: {pressure}, Location: {location}, Altitude: {altitude}")
        
        # Create a Point to write to InfluxDB
        point = (
            Point("weather_data")
            .tag("device", "esp32")
            .tag("location", location)
            .field("temperature", float(temperature))
            .field("humidity", float(humidity))
            .field("pressure", float(pressure))
            .field("altitude", float(altitude))
            .time(time.time_ns())  # Set the timestamp in nanoseconds
        )

        # Log the point to be written to InfluxDB
        logger.debug(f"Writing point to InfluxDB: {point.to_line_protocol()}")
        
        # Write data to InfluxDB
        write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=point)
        logger.info("Data successfully written to InfluxDB")
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")

# MQTT Client setup
client = mqtt.Client(client_id="WeatherMonitorSubscriber", protocol=mqtt.MQTTv311)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.tls_set()  # Secure connection (SSL/TLS)
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
try:
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_forever()
except Exception as e:
    logger.error(f"MQTT connection error: {str(e)}")
