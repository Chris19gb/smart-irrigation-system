import json
import os
import random
from datetime import datetime
from config import DATA_FOLDER

def fetch_ndvi_data():
    ndvi_data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "ndvi_index": round(random.uniform(0.2, 0.9), 3)  # Simulated NDVI Value
    }

    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    with open(os.path.join(DATA_FOLDER, 'ndvi_data.json'), 'w') as f:
        json.dump(ndvi_data, f, indent=4)

    print("NDVI data saved successfully.")

if __name__ == "__main__":
    fetch_ndvi_data()
