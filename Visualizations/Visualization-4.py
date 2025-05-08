# ========== Imports ==========
from influxdb_client import InfluxDBClient
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ========== InfluxDB Config ==========
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "K3yC8zERcrnJ0G7hEh_26caVuFA7xwhUzyEExy--cz2AUThswdPeMmubXc8E0XzzSRl9vWs4Sqze7JFN1UUFSw=="
INFLUX_ORG = "rowan"
BUCKET = "weatherdata"

# ========== Connect to InfluxDB ==========
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

# ========== Query Data ==========
query = f'''
from(bucket: "{BUCKET}")
  |> range(start: -30d)
  |> filter(fn: (r) => r._measurement == "weather_data")
  |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
  |> keep(columns: ["_time", "temperature", "humidity", "pressure", "altitude", "location", "device"])
  |> sort(columns: ["_time"])
'''

print("⏳ Querying InfluxDB...")
df = query_api.query_data_frame(org=INFLUX_ORG, query=query)
client.close()

# 🌦️ 5. Scatter Plot – Temperature vs. Humidity (Colored by Device)
plt.figure(figsize=(8, 6))
sns.scatterplot(data=df, x="temperature", y="humidity", hue="device")
plt.title("Temperature vs. Humidity")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.tight_layout()
plt.show()