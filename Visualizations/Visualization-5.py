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

# Two Separate Pie Charts (Inside vs Outside)

# Replace missing location values
df['location'] = df['location'].fillna('unknown')

# Filter for inside and outside
inside_df = df[df['location'].str.lower() == 'inside']
outside_df = df[df['location'].str.lower() == 'outside']

# Compute average for each sensor type
inside_means = inside_df[['temperature', 'humidity', 'pressure', 'altitude']].mean()
outside_means = outside_df[['temperature', 'humidity', 'pressure', 'altitude']].mean()

# Plot
fig, axes = plt.subplots(1, 2, figsize=(12, 6))

# Inside Pie
axes[0].pie(inside_means,
            labels=inside_means.index,
            autopct='%1.1f%%',
            colors=plt.cm.Pastel1.colors,
            startangle=90)
axes[0].set_title('Sensor Breakdown: Inside')

# Outside Pie
axes[1].pie(outside_means,
            labels=outside_means.index,
            autopct='%1.1f%%',
            colors=plt.cm.Pastel2.colors,
            startangle=90)
axes[1].set_title('Sensor Breakdown: Outside')

plt.tight_layout()
plt.show()

