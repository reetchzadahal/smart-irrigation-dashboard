import streamlit as st
import pandas as pd
import requests
import time
import datetime
import os
import firebase_admin
from firebase_admin import credentials, db
from flask import Flask, jsonify
from flask_cors import CORS
from threading import Thread

# --- 1. CONFIGURATION ---
ESP32_IP = "1.2.3.4" #IP adress of your arduino
URL = f"http://{ESP32_IP}"
MODEL_CSV = 'New_Weather.csv'
LOG_CSV = "Research_Log.csv"
FIREBASE_URL = "https://abc.firebasedatabase.app/" #your project's firebase url
WILTING_POINT = 35.0

# Global storage for the HTML dashboard to fetch
latest_stats = {
    "moisture": 0,
    "etc": 0,
    "pump_status": "OFF",
    "timestamp": ""
}

# --- 2. FIREBASE & DATA LOADING ---
if not firebase_admin._apps:
    try:
        if os.path.exists("firebase_key.json"):
            service_cred = credentials.Certificate("firebase_key.json")
            firebase_admin.initialize_app(service_cred, {'databaseURL': FIREBASE_URL})
    except Exception as e:
        print(f"Firebase Init Error: {e}")

@st.cache_data
def load_model_data():
    if os.path.exists(MODEL_CSV):
        df = pd.read_csv(MODEL_CSV)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        return df
    return pd.DataFrame()

model_df = load_model_data()

# --- 3. CORE LOGIC ENGINE ---
def process_data():
    global latest_stats
    try:
        # Get Sensor & Calibrate
        resp = requests.get(URL, timeout=3)
        raw_val = float(resp.text)
        pct = max(0, min(100, ((800 - raw_val) / 550) * 100))
        
        # Get Model Data
        today = datetime.date.today()
        match = model_df[model_df['Date'] == today]
        etc_val = match['ETc_Refined'].values[0] if not match.empty else (model_df['ETc_Refined'].iloc[0] if not model_df.empty else 0)

        # Automatic Pump Control Logic
        p_status = "ON" if pct < WILTING_POINT else "OFF"

        # Update global stats for the Bridge
        latest_stats = {
            "moisture": round(pct, 2),
            "etc": etc_val,
            "pump_status": p_status,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        }

        # Sync to Firebase
        if firebase_admin._apps:
            firebase_admin.db.reference('/tomato_data/current').set(latest_stats)
        
        return pct, etc_val
    except:
        return None, None

# --- 4. DATA ENGINE & BRIDGE ---
def process_data():
    global latest_stats
    try:
        # 1. Hardware Fetch
        resp = requests.get(URL, timeout=2)
        raw_val = float(resp.text)
        pct = max(0, min(100, ((800 - raw_val) / 550) * 100))
        
        # 2. Research Data Fetch (CSV)
        today = datetime.date.today()
        match = model_df[model_df['Date'] == today]
        etc_val = match['ETc_Refined'].values[0] if not match.empty else (model_df['ETc_Refined'].iloc[0] if not model_df.empty else 0)

        # 3. Decision Logic (Auto-Pump)
        p_status = "ON" if pct < WILTING_POINT else "OFF"

        # 4. Update the Stats for HTML
        latest_stats = {
            "moisture": round(pct, 1),
            "etc": round(etc_val, 2),
            "pump_status": p_status,
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S")
        }

        # 5. Cloud Sync
        if st.session_state.get('firebase_active'):
            firebase_admin.db.reference('/tomato_data/current').set(latest_stats)
        
        return pct, etc_val
    except:
        return None, None

# --- 5. MAIN LOOP ---
# This keeps the engine running in the background
while True:
    moisture, etc = process_data()
    if moisture is not None:
        st.toast(f"Data Synced: {moisture}% Moisture")
    time.sleep(3)
    st.rerun()
