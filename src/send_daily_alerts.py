import json
import pandas as pd
import requests
from datetime import datetime
from config import WEATHER_API_URL, WEATHER_API_KEY, LOCATION
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import csv
from dotenv import load_dotenv

# 🌱 Load .env variables
load_dotenv()

# Twilio Config
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# Email Config
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# 📘 Log alert to CSV
def log_alert(method, username, destination, message):
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "username": username,
        "method": method,
        "destination": destination,
        "message": message
    }
    log_file = "alert_log.csv"
    file_exists = os.path.isfile(log_file)

    with open(log_file, "a", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=log_entry.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(log_entry)

# 📲 Send SMS
def send_sms(to, body, username=""):
    try:
        to = str(to)
        if not to.startswith("+"):
            to = f"+{to}"
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(to=to, from_=TWILIO_PHONE_NUMBER, body=body)
        print(f"✅ SMS sent to {to}")
        log_alert("SMS", username, to, body)
    except Exception as e:
        print(f"⚠️ SMS failed for {to}: {e}")

# 📧 Send Email
def send_email(to_email, subject, message, username=""):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)

        print(f"✅ Email sent to {to_email}")
        log_alert("Email", username, to_email, message)
    except Exception as e:
        print(f"⚠️ Email failed to {to_email}: {e}")

# 🚨 Run Alert Check
def run_alert_check():
    print("🚀 Checking conditions for irrigation alerts...")

    try:
        response = requests.get(WEATHER_API_URL, params={'q': LOCATION, 'appid': WEATHER_API_KEY, 'units': 'metric'}, timeout=10)
        response.raise_for_status()
        weather = response.json()
    except Exception as e:
        print(f"❌ Failed to fetch weather data: {e}")
        return

    rainfall = weather.get("rain", {}).get("1h", 0) or 0

    with open("data/soil_moisture_data.json", "r") as f:
        soil = json.load(f)
    soil_moisture = soil['soil_moisture_percent']

    users = pd.read_csv("users.csv")

    for _, row in users.iterrows():
        username = row["username"]
        name = row["name"]
        phone = row["phone_number"]
        email = row.get("email", f"{username}@example.com")

        if soil_moisture < 30 and rainfall < 2:
            message = f"Hi {name}, soil moisture is low and no rainfall detected today. 💧 Please irrigate your farm."
        elif soil_moisture > 50 and rainfall > 2:
            message = f"Hi {name}, great news! 🌧️ Moisture levels and rainfall are optimal. No irrigation needed."
        else:
            message = f"Hi {name}, current conditions are moderate. 🌱 Stay alert for possible irrigation needs."

        send_sms(phone, message, username)
        send_email(email, "🌿 Smart Irrigation Alert", message, username)

if __name__ == "__main__":
    run_alert_check()
