# Smart Irrigation Dashboard - Final Clean Version
import streamlit as st
st.set_page_config(page_title="Smart Irrigation System", layout="wide")

from auth import validate_user, register_user, send_otp_sms, verify_otp, update_password
import requests
from config import WEATHER_API_URL, WEATHER_API_KEY, LOCATION
from twilio.rest import Client
import pandas as pd
import plotly.express as px
import folium, os, json, csv, time
from datetime import datetime
from streamlit_folium import st_folium
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# ------------------- REFRESH SETUP -------------------
REFRESH_INTERVAL = 300
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()
elif time.time() - st.session_state.last_refresh > REFRESH_INTERVAL:
    st.session_state.last_refresh = time.time()
    st.experimental_rerun()

# ------------------- SESSION INIT -------------------
for key in ["logged_in", "user_name", "username", "is_admin"]:
    if key not in st.session_state:
        st.session_state[key] = False if key == "logged_in" else ""

# ------------------- AUTH -------------------
menu = st.sidebar.selectbox("Choose Option", ["Login", "Register", "Forgot Password"])

if menu == "Login":
    st.sidebar.subheader("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        name = validate_user(username, password)
        if name:
            st.session_state.logged_in = True
            st.session_state.user_name = name
            st.session_state.username = username
            st.session_state.is_admin = username.lower() == "admin"
            st.sidebar.success(f"Welcome, {name} 👋")
        else:
            st.sidebar.error("Invalid username or password")

elif menu == "Register":
    st.sidebar.subheader("Register")
    new_username = st.sidebar.text_input("Choose a Username")
    new_name = st.sidebar.text_input("Your Full Name")
    new_password = st.sidebar.text_input("Choose a Password", type="password")
    new_phone = st.sidebar.text_input("Your Phone Number (e.g., +265...)")
    new_email = st.sidebar.text_input("Your Email Address")
    if st.sidebar.button("Register"):
        if register_user(new_username, new_name, new_password, new_phone, new_email):
            st.sidebar.success("Registered successfully!")
        else:
            st.sidebar.warning("Username already exists.")

elif menu == "Forgot Password":
    st.sidebar.subheader("Reset Your Password")
    username_reset = st.sidebar.text_input("Enter your username")
    if st.sidebar.button("Send OTP"):
        users_df = pd.read_csv("users.csv")
        user_row = users_df[users_df["username"] == username_reset]
        if not user_row.empty:
            phone = user_row.iloc[0]["phone_number"]
            send_otp_sms(username_reset, phone)
            st.session_state.reset_user = username_reset
            st.session_state.otp_sent = True
            st.sidebar.success("✅ OTP sent to your phone.")
        else:
            st.sidebar.error("❌ Username not found.")
    if st.session_state.get("otp_sent"):
        code = st.sidebar.text_input("Enter OTP Code")
        new_pass = st.sidebar.text_input("New Password", type="password")
        confirm_pass = st.sidebar.text_input("Confirm Password", type="password")
        if st.sidebar.button("Reset Password"):
            if new_pass != confirm_pass:
                st.sidebar.warning("Passwords do not match.")
            elif verify_otp(st.session_state.reset_user, code):
                update_password(st.session_state.reset_user, new_pass)
                st.sidebar.success("✅ Password reset successfully.")
                st.session_state.otp_sent = False
            else:
                st.sidebar.error("❌ Invalid or expired OTP.")

# ------------------- MAIN DASHBOARD -------------------
if st.session_state.logged_in:
    if st.session_state.is_admin:
        st.markdown("### Admin Panel: Alert Log")
        log_path = "alert_log.csv"
        if os.path.exists(log_path):
            log_df = pd.read_csv(log_path)
            log_df["timestamp"] = pd.to_datetime(log_df["timestamp"], format="%d/%m/%Y %H:%M", dayfirst=False, errors="coerce")
            st.dataframe(log_df.sort_values(by="timestamp", ascending=False), use_container_width=True)
        else:
            st.info("No alert logs yet.")

    st.markdown("""
        <style>.main-title { font-size: 30px; font-weight: bold; color: #2a9d8f; }</style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="main-title">Smart Irrigation System Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")

    def fetch_live_weather():
        params = {'q': LOCATION, 'appid': WEATHER_API_KEY, 'units': 'metric'}
        try:
            response = requests.get(WEATHER_API_URL, params=params)
            response.raise_for_status()
            return response.json()
        except:
            if os.path.exists("data/weather_data.json"):
                with open("data/weather_data.json") as f:
                    return json.load(f)
            else:
                st.error("❌ No weather data available.")
                st.stop()

    weather_data = fetch_live_weather()
    with open("data/weather_data.json", "w") as f:
        json.dump(weather_data, f, indent=4)

    # --- Weather Values ---
    temp = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    pressure = weather_data['main']['pressure']
    wind_speed = weather_data['wind']['speed']
    weather_condition = weather_data['weather'][0]['description']
    rainfall = weather_data.get("rain", {}).get("1h", 0) or 0

    # --- Soil & NDVI Data ---
    with open("data/soil_moisture_data.json") as f:
        soil_data = json.load(f)
    with open("data/ndvi_data.json") as f:
        ndvi_data = json.load(f)

    # --- Weather Overview ---
    st.markdown("###  Weather Summary - Mzuzu")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(" Temp (°C)", temp)
    col2.metric(" Humidity", humidity)
    col3.metric(" Pressure", pressure)
    col4.metric(" Wind", wind_speed)
    col5.metric(" Rainfall", rainfall)
    st.info(f"Condition: **{weather_condition.title()}**")
    st.plotly_chart(px.bar(pd.DataFrame({
        "Parameter": ["Temperature", "Humidity", "Pressure", "Wind Speed"],
        "Values": [temp, humidity, pressure, wind_speed]
    }), x="Parameter", y="Values", color="Parameter", title="Weather Overview",
    color_discrete_sequence=["#f4a261", "#2a9d8f", "#264653", "#e9c46a"]))

    # --- Trends ---
    def render_trend(title, path, value_col, color):
        if os.path.exists(path):
            df = pd.read_csv(path, parse_dates=["timestamp"], dayfirst=False)
            df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=False, errors="coerce")
            df["date"] = df["timestamp"].dt.date
            last_7 = df[df["date"] >= (datetime.now().date() - pd.Timedelta(days=7))]
            st.markdown(f"### {title}")
            if not last_7.empty:
                st.plotly_chart(px.bar(
                    last_7, x="date", y=value_col, color=value_col,
                    color_continuous_scale=color,
                    title=f"{title} - Bar Chart"
                ))
                st.plotly_chart(px.line(
                    last_7, x="date", y=value_col,
                    title=f"{title} - Line Chart",
                    markers=True
                ))
            else:
                st.info("No data for the last 7 days.")
        else:
            st.info(f"{title} data not available.")

    render_trend(" Rainfall Trend", "data/rainfall_log.csv", "rainfall_mm", "Blues")
    render_trend(" Temperature Trend", "data/temperature_log.csv", "temperature", "OrRd")
    render_trend(" Soil Moisture Trend", "data/soil_log.csv", "soil_moisture_percent", "YlGn")
    render_trend(" NDVI Trend", "data/ndvi_log.csv", "ndvi_index", "Greens")
    render_trend(" Humidity Trend", "data/humidity_log.csv", "humidity", "PuBu")

    # --- KPIs ---
    st.markdown("###  Smart Irrigation KPIs")
    k1, k2, k3 = st.columns(3)
    k1.metric("Soil", "Low" if soil_data['soil_moisture_percent'] < 30 else "Optimal")
    k2.metric("NDVI", "Poor" if ndvi_data['ndvi_index'] < 0.4 else "Healthy")
    k3.metric("Rainfall", f"{rainfall} mm")
    st.divider()

    # --- Pie + NDVI ---
    st.markdown("### 💧 Soil Moisture")
    st.metric("Moisture (%)", soil_data["soil_moisture_percent"])
    st.caption(f"Last Recorded: {soil_data['timestamp']}")
    st.plotly_chart(px.pie(
        values=[soil_data['soil_moisture_percent'], 100 - soil_data['soil_moisture_percent']],
        names=["Moisture", "Dry"],
        color_discrete_sequence=["#2a9d8f", "#e76f51"],
        title="Soil Moisture Distribution"
    ))

    st.markdown("###  NDVI Health")
    st.metric("NDVI Index", ndvi_data['ndvi_index'])
    st.caption(f"Last Recorded: {ndvi_data['timestamp']}")
    st.plotly_chart(px.bar(x=["NDVI"], y=[ndvi_data['ndvi_index']],
                           color_discrete_sequence=["green"], title="NDVI Index"))

    # --- NDVI Heatmap ---
    st.markdown("### 🟩 NDVI Heatmap (Simulated)")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(np.random.uniform(0.2, 0.9, (10, 10)), cmap="Greens", ax=ax)
    st.pyplot(fig)

    # --- Recommendation ---
    st.markdown("###  Irrigation Recommendation")
    if soil_data['soil_moisture_percent'] < 30 and rainfall < 2:
        st.error("Soil is dry and no rain detected. Irrigation needed.")
    elif soil_data['soil_moisture_percent'] > 50 and rainfall > 2:
        st.success("Moisture and rain levels are good.")
    else:
        st.info("Monitor conditions—irrigation might be needed soon.")

    # --- Map ---
    st.markdown("###  Farm Location Map")
    m = folium.Map(location=[-11.45422, 34.04358], zoom_start=13)
    folium.Marker([-11.45422, 34.04358],
                  popup=f"Soil: {soil_data['soil_moisture_percent']}% | NDVI: {ndvi_data['ndvi_index']}",
                  tooltip="Farm").add_to(m)
    st_folium(m, width=700, height=450)

    st.success("✅ Dashboard Loaded Successfully!")

else:
    st.warning("👈 Please log in or register to view the dashboard.")
