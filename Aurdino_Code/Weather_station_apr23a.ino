#include "arduino_secrets.h"
#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <ArduinoJson.h>  // Include ArduinoJson library

// WiFi Credentials
const char* ssid = "Poyaam_Mosam";
const char* password = "Shaik4you";

// HiveMQ Cloud
const char* mqttServer = "29149bc39a6c4a8890d51c27de41a970.s1.eu.hivemq.cloud";
const int mqttPort = 8883;
const char* mqttUser = "Sindhu";
const char* mqttPassword = "Sindhu13";

// MQTT topic
const char* topic = "weather/esp32";

// Sensor and MQTT clients
WiFiClientSecure espClient;
PubSubClient client(espClient);
Adafruit_BME280 bme;

float temperature, humidity, pressure, altitude;
String location;

void setupWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
}

void connectToMQTT() {
  // Set insecure (you can load your own certificate if needed)
  espClient.setInsecure(); 

  client.setServer(mqttServer, mqttPort);

  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect("WeatherClient", mqttUser, mqttPassword)) {
      Serial.println("connected!");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  setupWiFi();
  connectToMQTT();

  if (!bme.begin(0x77)) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    while (1);
  } else {
    Serial.println("BME280 initialized.");
  }
}

void loop() {
  if (!client.connected()) {
    connectToMQTT();
  }
  client.loop();

  // Read BME280
  temperature = bme.readTemperature();
  humidity = bme.readHumidity();
  pressure = bme.readPressure() / 100.0F;// convert pa to hpa

  float seaLevelPressure = 1023.00;// in hpa
  altitude = 44330.0 * (1.0 - pow(pressure / seaLevelPressure, 1.0 / 5.255));// in meters
  location = (temperature > 25) ? "Outside": "Inside";

  // Create a JSON object using ArduinoJson
  StaticJsonDocument<200> doc;
  doc["temperature"] = temperature;
  doc["humidity"] = humidity;
  doc["pressure"] = pressure;
  doc["altitude"] = altitude;
  doc["location"] = location;

  // Serialize the JSON document to a string
  String payload;
  serializeJson(doc, payload);

  Serial.println("Publishing: " + payload);
  client.publish(topic, payload.c_str());

  delay(60000);
}

/*
  Since Location is READ_WRITE variable, onLocationChange() is
  executed every time a new value is received from IoT Cloud.
*/
void onLocationChange()  {
  // Add your code here to act upon Location change
}