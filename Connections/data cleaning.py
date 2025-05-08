from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import pandas as pd

# InfluxDB connection details
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "K3yC8zERcrnJ0G7hEh_26caVuFA7xwhUzyEExy--cz2AUThswdPeMmubXc8E0XzzSRl9vWs4Sqze7JFN1UUFSw=="
INFLUX_ORG = "rowan"
SOURCE_BUCKET = "mybucket"
TARGET_BUCKET = "weatherdata"

# Connect to InfluxDB
client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

# Query past 6 days of data from the source bucket
query = f'''
from(bucket: "{SOURCE_BUCKET}")
  |> range(start: -10d)
  |> filter(fn: (r) => r._measurement == "weather_data")
'''

# Get the query result
tables = query_api.query(query)

# Check if tables are returned
if not tables:
    print("No data found.")
    client.close()
    exit()

# Process the query result and convert to DataFrame manually
records = []
for table in tables:
    for record in table.records:
        record_dict = record.values
        record_dict['_time'] = record.get_time()  # Add time as a column
        records.append(record_dict)

# Convert records to DataFrame
df = pd.DataFrame(records)
print(f"Raw rows: {len(df)}")

# Data Cleaning
df_clean = df.dropna(subset=["_value"])                            # Remove NaNs
df_clean = df_clean[df_clean["_value"] > 0]                        # Remove values <= 0
df_clean = df_clean[~((df_clean["_field"] == "altitude") & 
                      (df_clean["_value"] < 25))]                 # Remove altitude < 25
df_clean["_time"] = pd.to_datetime(df_clean["_time"])             # Ensure datetime format

print(f"Cleaned rows: {len(df_clean)}")

# Write cleaned data to new bucket
write_api = client.write_api(write_options=SYNCHRONOUS)
for _, row in df_clean.iterrows():
    point = (
        Point(row["_measurement"])
        .tag("device", row.get("device", "esp32"))
        .tag("location", row.get("location", "unknown"))
        .field(row["_field"], float(row["_value"]))
        .time(row["_time"], WritePrecision.NS)
    )
    write_api.write(bucket=TARGET_BUCKET, org=INFLUX_ORG, record=point)

print(f"✅ {len(df_clean)} cleaned records written to '{TARGET_BUCKET}'.")

client.close()
