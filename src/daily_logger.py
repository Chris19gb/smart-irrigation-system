import json
import requests
import pandas as pd
import os
from datetime import datetime
from config import WEATHER_API_URL, WEATHER_API_KEY, LOCATION

# Load soil and NDVI data
with open("data/soil_moisture_data.json") as f:
    soil_data = json.load(f)
with open("data/ndvi_data.json") as f:
    ndvi_data = json.load(f)

# Fetch weather data
response = requests.get(WEATHER_API_URL, params={"q": LOCATION, "appid": WEATHER_API_KEY, "units": "metric"})
if response.status_code == 200:
    weather = response.json()
    temp = weather['main']['temp']
    humidity = weather['main']['humidity']
    rainfall = weather.get("rain", {}).get("1h", 0) or weather.get("rain", {}).get("3h", 0) or 0
else:
    print("❌ Failed to fetch weather data.")
    exit()

# ✅ Clean logging function
def log_to_csv(path, data, columns):
    today = datetime.now().date()
    log_entry = {"timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), **data}

    if os.path.exists(path):
        df = pd.read_csv(path)
        df["timestamp"] = pd.to_datetime(df["timestamp"], format="%d/%m/%Y %H:%M", errors="coerce")
        #df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=True, errors="coerce")
        #df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")  # Auto detect format
        df["date"] = df["timestamp"].dt.date

        if today in df["date"].values:
            return  # Already logged today

        df = df.drop(columns=["date"])
        df = pd.concat([df, pd.DataFrame([log_entry])], ignore_index=True)
    else:
        df = pd.DataFrame([log_entry], columns=["timestamp"] + columns)

    df.to_csv(path, index=False)

# 🚀 Run logs
log_to_csv("data/temperature_log.csv", {"temperature": temp}, ["temperature"])
log_to_csv("data/humidity_log.csv", {"humidity": humidity}, ["humidity"])
log_to_csv("data/rainfall_log.csv", {"rainfall_mm": rainfall}, ["rainfall_mm"])
log_to_csv("data/ndvi_log.csv", {"ndvi_index": ndvi_data["ndvi_index"]}, ["ndvi_index"])
log_to_csv("data/soil_log.csv", {"soil_moisture_percent": soil_data["soil_moisture_percent"]}, ["soil_moisture_percent"])

print("✅ Daily logging completed.")
