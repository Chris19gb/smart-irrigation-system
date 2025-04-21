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


