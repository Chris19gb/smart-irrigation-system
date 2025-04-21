import json
import os
from config import DATA_FOLDER

def load_weather_data():
    file_path = os.path.join(DATA_FOLDER, 'weather_data.json')

    if not os.path.exists(file_path):
        print("No weather data found. Please run fetch_weather_data.py first.")
        return None

    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def process_weather_data():
    data = load_weather_data()

    if data is None:
        return

    processed = {
        'City': data['name'],
        'Temperature': data['main']['temp'],
        'Humidity': data['main']['humidity'],
        'Pressure': data['main']['pressure'],
        'Wind Speed': data['wind']['speed'],
        'Weather': data['weather'][0]['description'],
    }

    print("Processed Weather Data:")
    print(processed)

if __name__ == "__main__":
    process_weather_data()
