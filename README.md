# **🌤️ Smart Weather Station IoT Project**
# **🌦️ IoT Weather Station – Arduino + MQTT + InfluxDB + Grafana/VS Code**
# 📝 Project Overview
This project implements a Smart Weather Station using an ESP32 microcontroller and a BME280 environmental sensor. It collects real-time environmental data — temperature, humidity, pressure, altitude, and location (from Arduino IoT Cloud).

The data is transmitted via the MQTT protocol (HiveMQ Cloud) and ingested into an InfluxDB time-series database. A Python pipeline then cleans and filters this data, storing the results in a separate bucket for analysis and visualization using Grafana dashboards and custom ML plots in Visual Studio Code.
# 🛠️ Components
# Hardware:
- HiLetgo ESP-WROOM-32 (ESP32) board
- Waveshare BME280 sensor (Temperature, Pressure, Humidity, Altitude)
# Software & Tools:
- Arduino Iot cloud website (for programming ESP32)
- Python through vscode (for data cleaning)
- HiveMQ Cloud (MQTT broker)
- Docker to create Influxdb containers
- InfluxDB (for time-series data storage)
- Grafana (for visualization)
- VS code (for Visualization using ML codes)
# 🧱 System Architecture
| Layer           | Tool/Service                        |
| --------------- | ----------------------------------- |
| Sensor          | BME280                              |
| Microcontroller | HiLetgo ESP-WROOM-32 (ESP32)        |
|Software         | Arduino Iot cloud website           |
| Protocol        | MQTT (via HiveMQ Cloud)             |
|Containers       | Docker                              |
| Data Ingestion  | Python (paho-mqtt, influxdb-client) |
| Storage         | InfluxDB                            |
| Visualization   | Grafana                             |

# **📡 Data Flow**
- ESP32 + BME280 Sensor  
        ↓ (via MQTT)  
- HiveMQ Cloud  
        ↓  
- Python MQTT Client  
        ↓  
- InfluxDB (Raw Data — Bucket: `mybucket`)  
        ↓ (Python Cleaning Script)  
- InfluxDB (Cleaned Data — Bucket: `weatherdata`)  
        ↓  
- Visualization (Grafana) + ML (VS Code)
# 🧪 Key Features
- ✅ Real-time environmental data collection
- 🔒 Secure MQTT communication (TLS/SSL)
- 📥 Efficient ingestion into InfluxDB
- 🧹 Data cleaning pipeline:
Remove NaN values
- Filter outliers (e.g., altitude < 25m)
- 📊 Visualization options:
Grafana dashboards
Python ML charts (bar, line, scatter, heatmap)
- 📂 Clean modular project structure
# 📅 Data Collection Details
- The data was collected at a 1-minute time interval on different days.
- Total Rows Collected: 1115
- Inside: 453 rows
- Outside: 703 rows
# 🐍 Python Scripts
| Script Name          | Description                                                                                                    |
| -------------------- | -------------------------------------------------------------------------------------------------------------- |
| `MQTT.py`            | Subscribes to HiveMQ Cloud broker, listens to ESP32 topic, parses JSON data                                    |
| `INFLUX.py`          | Writes parsed sensor data to InfluxDB (bucket: `mybucket`)                                                     |
| `data cleaning.py`   | Cleans raw data (e.g., filters out altitude < 25m, removes invalid entries) and writes to `weatherdata` bucket |
| `Visualization-1.py` | Creates 🌡️ Heatmap – Correlation Between All Numeric Features                                                 |
| `Visualization-2.py` | Plots Pressure vs Altitude scatter plot, Line graph: Temperature Over Time                                     |
| `Visualization-3.py` | 🕓 Histogram – Distribution of Pressure                                                                        |
| `Visualization-4.py` | 🌦️ Scatter Plot – Temperature vs. Humidity (Colored by Device)                                                |
| `Visualization-5.py` | Two Separate Pie Charts (Inside vs Outside)                                                                    |
# 📊 Grafana Dashboards
- We created multiple visualizations to explore trends, comparisons, and patterns:
- Humidity Over Time & Locations
- Humidity vs Pressure at Different Locations
- Humidity vs Temperature (Line Chart)
- Pressure vs Altitude
- Temperature vs Humidity (Bar Chart)
- Weather vs Time

## 📂  Directory Structure
```bash
.
├── Aurdino_Code/
│   ├── Weather_station_apr23a.ino       # Main Arduino sketch
│   ├── arduino_secrets.h                # Wi-Fi and MQTT credentials
│   ├── sketch.json                      # Arduino Cloud sketch config
│   ├── thingProperties.h                # Arduino IoT property setup
│   └── ReadMe.adoc                      # Arduino-specific documentation
│
├── Connections/
│   ├── MQTT.py                          # MQTT subscriber to HiveMQ
│   ├── INFLUX.PY                        # Writes MQTT data into InfluxDB
│   └── data cleaning.py                 # Cleans data before writing to DB
│
├── Visualizations/
│   ├── Visualization-1.py               # Temperature vs Humidity (Bar)
│   ├── Visualization-2.py               # Pressure vs Altitude
│   ├── Visualization-3.py               # Humidity vs Temperature (Line)
│   ├── Visualization-4.py               # Humidity vs Pressure
│   └── Visualization-5.py               # Weather vs Time
│
├── Grafana/
│   └── Visualization links in grafana.pdf  # Screenshot/links to dashboards
│
├── README.md                            # Project documentation
```
# 🐬 MySQL Container Setup (Windows)
- To set up a local MySQL container with Docker:
- 📁 Step-by-Step
```
docker run --name mysql -d ^
    -p 3306:3306 ^
    -e MYSQL_ROOT_PASSWORD=root-pwd ^
    -e MYSQL_ROOT_HOST="%" ^
    -e MYSQL_DATABASE=mydb ^
    -e MYSQL_USER=remote_user ^
    -e MYSQL_PASSWORD=remote_user-pwd ^
    docker.io/library/mysql:8.4.4
- 🐳 Create and Run Container
```
docker run -d -p 8086:8086 \
  --name myinflux \
  -v "$PWD/data:/var/lib/influxdb2" \
  -v "$PWD/config:/etc/influxdb2" \
  -e DOCKER_INFLUXDB_INIT_MODE=setup \
  -e DOCKER_INFLUXDB_INIT_USERNAME=admin \
  -e DOCKER_INFLUXDB_INIT_PASSWORD=P@ssw0rd1 \
  -e DOCKER_INFLUXDB_INIT_ORG=rowan \
  -e DOCKER_INFLUXDB_INIT_BUCKET=mybucket \
  -e DOCKER_INFLUXDB_INIT_RETENTION=1h \
  docker.io/library/influxdb:latest
# 📂 Flux Queries (InfluxDB)
- 🔍 1. Query from Raw Data (mybucket bucket)  
```flux
from(bucket: "mybucket")
  |> range(start: -30d)
  |> filter(fn: (r) => r._measurement == "weather_data")
  |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> keep(columns: ["_time", "temperature", "humidity", "pressure", "altitude", "location", "device"])
  |> sort(columns: ["_time"])
- 🧪 2. Query from Cleaned Data (weatherdata bucket)
```flux
from(bucket: "weatherdata")
  |> range(start: -30d)
  |> filter(fn: (r) => r._measurement == "weather_data")
  |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> keep(columns: ["_time", "temperature", "humidity", "pressure", "altitude", "location", "device"])
  |> filter(fn: (r) => exists r.temperature and exists r.humidity and exists r.pressure and exists r.altitude)
  |> sort(columns: ["_time"])
- 🧮 3. Count Temperature Rows (from Cleaned Bucket)
```flux
from(bucket: "weatherdata")
  |> range(start: -30d)
  |> filter(fn: (r) => r._measurement == "weather_data")
  |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> keep(columns: ["_time", "temperature", "humidity", "pressure", "altitude", "location", "device"])
  |> filter(fn: (r) => exists r.temperature and exists r.humidity and exists r.pressure and exists r.altitude)
  |> count(column: "temperature")
# 🐳 Docker Networking (Grafana + InfluxDB)
- docker network create my_network
- docker network connect my_network myinfluxdbs
- docker network connect my_network mygrafana
- **Note:** run these commands in windows powershell.
