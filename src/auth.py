import pandas as pd
import hashlib
import os
import json
import random
import time
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Paths
USERS_FILE = "users.csv"
OTP_FILE = "otp_store.json"

# Load environment variables securely
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


# ---------------------- User Management ----------------------
def load_users():
    if not os.path.exists(USERS_FILE):
        df = pd.DataFrame(columns=["username", "name", "password", "phone_number", "email"])
        df.to_csv(USERS_FILE, index=False)
    return pd.read_csv(USERS_FILE)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def validate_user(username, password):
    users = load_users()
    hashed = hash_password(password)
    user_row = users[(users["username"] == username) & (users["password"] == hashed)]
    if not user_row.empty:
        return user_row.iloc[0]["name"]
    return None


def user_exists(username):
    users = load_users()
    return username in users["username"].values


def register_user(username, name, password, phone_number, email):
    if user_exists(username):
        return False
    users = load_users()
    new_user = pd.DataFrame([[username, name, hash_password(password), phone_number, email]],
                            columns=["username", "name", "password", "phone_number", "email"])
    users = pd.concat([users, new_user], ignore_index=True)
    users.to_csv(USERS_FILE, index=False)
    return True


# ---------------------- OTP SMS ----------------------
def send_otp_sms(username, phone):
    otp_code = str(random.randint(100000, 999999))
    otp_entry = {
        "code": otp_code,
        "timestamp": time.time()
    }

    # Save OTP for the user
    if os.path.exists(OTP_FILE):
        with open(OTP_FILE, "r") as f:
            otp_store = json.load(f)
    else:
        otp_store = {}

    otp_store[username] = otp_entry
    with open(OTP_FILE, "w") as f:
        json.dump(otp_store, f, indent=4)

    # Send OTP via SMS
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            to=phone if phone.startswith("+") else f"+{phone}",
            from_=TWILIO_PHONE_NUMBER,
            body=f"🔐 Your OTP Code is: {otp_code}"
        )
        print(f"[OTP Sent] to {phone} - Code: {otp_code}")
    except Exception as e:
        print(f"❌ Failed to send OTP SMS: {e}")


# ---------------------- OTP Verification ----------------------
def verify_otp(username, code):
    if not os.path.exists(OTP_FILE):
        return False

    with open(OTP_FILE, "r") as f:
        otp_store = json.load(f)

    if username in otp_store:
        entry = otp_store[username]
        if entry["code"] == code and time.time() - entry["timestamp"] < 300:  # 5 minutes
            del otp_store[username]  # One-time use
            with open(OTP_FILE, "w") as f:
                json.dump(otp_store, f, indent=4)
            return True

    return False


# ---------------------- Password Update ----------------------
def update_password(username, new_password):
    users = load_users()
    users.loc[users["username"] == username, "password"] = hash_password(new_password)
    users.to_csv(USERS_FILE, index=False)
