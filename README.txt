# 🌿 Smart Irrigation System Dashboard

A real-time, intelligent irrigation monitoring and alert system for farmers — powered by Streamlit, weather/NDVI APIs, and automated SMS/Email alerts.
---

## 🚀 Features

- 📡 **Live Weather Monitoring** (Temperature, Rainfall, Humidity, Wind)
- 🌱 **Soil Moisture & NDVI Health Visualization**
- 📊 **Daily Trends Graphs** (Rainfall, Temperature, Humidity, NDVI, Soil Moisture)
- 🔁 **Automated Daily Logging**
- 📲 **SMS + Email Alerts** for farmers based on real-time field conditions
- 👥 **User Registration & Login**
- 🔐 **Password Reset via OTP**
- 🛡️ **Admin Panel** for tracking all sent alerts

---

## 🔧 Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Backend:** Python, Pandas, Folium, Plotly, Seaborn
- **APIs:** OpenWeatherMap, Google Earth Engine (NDVI), SMAP (Soil Moisture)
- **Notifications:** Twilio (SMS), Gmail SMTP (Email)
- **Data Storage:** CSV-based logs (`data/` folder)
- **Automation:** GitHub Actions (Daily logging and alert scheduling)

---

## 📂 Project Structure

smart_irrigation_system_project/ ├── .streamlit/ # Streamlit config ├── src/ │ ├── app.py # Main dashboard app │ ├── auth.py # User auth & OTP logic │ ├── config.py # API keys (via .env) │ ├── daily_logger.py # Logs weather/NDVI/soil data daily │ ├── send_daily_alerts.py # Sends SMS/Email alerts │ ├── fetch_*.py # Fetches weather, NDVI, soil moisture │ ├── data/ # Contains CSV + JSON logs │ └── users.csv # User records ├── .env # 🔒 Secrets (not pushed to GitHub) ├── .gitignore ├── requirements.txt └── README.md
## ⚙️ Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/smart-irrigation-system.git
   cd smart-irrigation-system/src

## Create a virtual environment (recommended)
 '''bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/macOS

## Install dependencies
pip install -r ../requirements.txt

## Create .env file inside src/ directory
Add the following and replace with your actual values:
WEATHER_API_KEY=your_openweather_api_key
WEATHER_API_URL=https://api.openweathermap.org/data/2.5/weather
LOCATION=Mzuzu
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
EMAIL_SENDER=youremail@gmail.com
EMAIL_PASSWORD=your_email_app_password

## Run the dashboard
streamlit run app.py

## Scheduled Tasks
daily_logger.py: Logs weather, NDVI, soil moisture, etc. once per day.

send_daily_alerts.py: Sends SMS and Email alerts to all registered users.
## GitHub Actions Setup (Auto run daily):
See .github/workflows/daily_tasks.yml to configure scheduled GitHub Actions to automate daily logging and alerts.

## Deployment
You can deploy this dashboard easily via:

1.Streamlit Cloud (recommended)

2.Docker or VPS

3.GitHub Actions for automation

## Credits 
1.NDVI & Soil APIs: NASA/Google Earth Engine (custom pipeline)

2.Weather API: OpenWeatherMap

3.SMS: Twilio

4.Email: Gmail SMTP with App Passwords

## Contact
Developer: Christopher G.
Email: macdalfchristopher@gmail.com
GitHub: Chris19gb

## License
This project is licensed under the MIT License. Feel free to use and contribute!


