import json
import os
import random
from datetime import datetime
from config import DATA_FOLDER

def fetch_ndvi_data():
    try:
        ndvi_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ndvi_index": round(random.uniform(0.2, 0.9), 3)  # Simulated NDVI value
        }

        os.makedirs(DATA_FOLDER, exist_ok=True)

        file_path = os.path.join(DATA_FOLDER, 'ndvi_data.json')
        with open(file_path, 'w') as f:
            json.dump(ndvi_data, f, indent=4)

        print(f"✅ NDVI data saved successfully at {file_path}")

    except Exception as e:
        print("❌ Failed to generate NDVI data:", str(e))

if __name__ == "__main__":
    fetch_ndvi_data()
