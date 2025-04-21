
import requests
import json
import pandas as pd
import os
from datetime import datetime
from config import WEATHER_API_URL, WEATHER_API_KEY, LOCATION, DATA_FOLDER
from dotenv import load_dotenv
load_dotenv()
def fetch_weather():
    params = {
        'q': LOCATION,
        'appid': WEATHER_API_KEY,
        'units': 'metric'
    }

    response = requests.get(WEATHER_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        os.makedirs(DATA_FOLDER, exist_ok=True)

        # Save JSON
        with open(os.path.join(DATA_FOLDER, 'weather_data.json'), 'w') as f:
            json.dump(data, f, indent=4)

        # Extract rainfall
        rain = data.get("rain", {}).get("1h", 0) or data.get("rain", {}).get("3h", 0) or 0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Append to CSV log
        log_path = os.path.join(DATA_FOLDER, 'rainfall_log.csv')
        df = pd.DataFrame([[timestamp, rain]], columns=["timestamp", "rainfall_mm"])

        if os.path.exists(log_path):
            df.to_csv(log_path, mode='a', header=False, index=False)
        else:
            df.to_csv(log_path, index=False)

        print("Weather + Rainfall data saved successfully.")

    else:
        print("Failed to fetch weather data:", response.status_code)

if __name__ == "__main__":
    fetch_weather()




