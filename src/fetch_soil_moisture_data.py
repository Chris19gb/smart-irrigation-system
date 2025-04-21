import json
import os
import random
from datetime import datetime
from config import DATA_FOLDER

def fetch_soil_moisture_data():
    soil_moisture_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "soil_moisture_percent": round(random.uniform(10, 50), 2)  # Simulated %
    }

    # Ensure output folder exists
    os.makedirs(DATA_FOLDER, exist_ok=True)

    output_path = os.path.join(DATA_FOLDER, "soil_moisture_data.json")
    with open(output_path, "w") as f:
        json.dump(soil_moisture_data, f, indent=4)

    print("Soil moisture data saved successfully.")

if __name__ == "__main__":
    fetch_soil_moisture_data()
