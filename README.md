**🌤️ Smart Weather Station IoT Project**
**🌦️ IoT Weather Station – Arduino + MQTT + InfluxDB + Grafana/VS Code**
**Project Overview**
This project implements a Smart Weather Station using an ESP32 microcontroller and a BME280 environmental sensor. It collects real-time environmental data — temperature, humidity, pressure, and altitude, location in aurdino iot cloud website. Now this data will be send to an InfluxDB time-series database using MQTT protocol via HiveMQ Cloud. A Python pipeline then cleans and filters the data before storing it into a new bucket for analysis and visualized through Grafana dashboards and custom ML plots in Visual studio code.
🛠️ Components
**Hardware:**
HiLetgo ESP-WROOM-32 (ESP32) board
Waveshare BME280 sensor (Temperature, Pressure, Humidity, Altitude)
**Software & Tools:**
Arduino Iot cloud website (for programming ESP32)
Python through vscode (for data cleaning)
HiveMQ Cloud (MQTT broker)
Docker to create Influxdb containers
InfluxDB (for time-series data storage)
Grafana (for visualization)
VS code (for Visualization using ML codes)
**📡 Data Flow**
ESP32 + BME280 Sensor
        ↓ (via MQTT)
     HiveMQ Cloud
        ↓
    Python MQTT Client 
        ↓
   InfluxDB (Raw Data - Bucket: `mybucket`)
        ↓ (Python Cleaning Script)
   InfluxDB (Cleaned Data - Bucket: `weatherdata`)
        ↓
   Visualization(grafana) + ML(VS code)

   | Layer           | Tool/Service                        |
| --------------- | ----------------------------------- |
| Sensor          | BME280                              |
| Microcontroller | HiLetgo ESP-WROOM-32 (ESP32)        |
| Protocol        | MQTT (via HiveMQ Cloud)             |
| Data Ingestion  | Python (paho-mqtt, influxdb-client) |
| Storage         | InfluxDB                            |
| Visualization   | Grafana                             |

