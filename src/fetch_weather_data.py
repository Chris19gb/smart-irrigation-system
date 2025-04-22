import requests
import json
import pandas as pd
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load config values safely
WEATHER_API_URL = os.getenv("WEATHER_API_URL", "https://api.openweathermap.org/data/2.5/weather")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
LOCATION = os.getenv("LOCATION", "Karonga")
DATA_FOLDER = os.getenv("DATA_FOLDER", "data")

def fetch_weather():
    if not WEATHER_API_KEY:
        print("❌ WEATHER_API_KEY is missing! Check your .env or secrets.")
        return

    params = {
        'q': LOCATION,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(WEATHER_API_URL, params=params, timeout=10)

        if response.status_code == 200:
            data = response.json()
            os.makedirs(DATA_FOLDER, exist_ok=True)

            # Save JSON
            with open(os.path.join(DATA_FOLDER, 'weather_data.json'), 'w') as f:
                json.dump(data, f, indent=4)

            # Extract rainfall
            rain = data.get("rain", {}).get("1h") or data.get("rain", {}).get("3h") or 0
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Append to CSV log
            log_path = os.path.join(DATA_FOLDER, 'rainfall_log.csv')
            df = pd.DataFrame([[timestamp, rain]], columns=["timestamp", "rainfall_mm"])

            if os.path.exists(log_path):
                df.to_csv(log_path, mode='a', header=False, index=False)
            else:
                df.to_csv(log_path, index=False)

            print("✅ Weather + Rainfall data saved successfully.")

        else:
            print(f"❌ Failed to fetch weather data: {response.status_code}")
            print(f"🔍 Response content: {response.text}")

    except Exception as e:
        print("❌ Error while fetching weather data:", str(e))

if __name__ == "__main__":
    fetch_weather()

