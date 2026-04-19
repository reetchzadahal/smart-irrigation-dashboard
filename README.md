# Smart Irrigation Dashboard

## Overview

This project implements a smart irrigation system using IoT and data modeling techniques.

It combines:

* Real-time soil moisture sensing (ESP32)
* Historical weather data
* Evapotranspiration (ET) modeling

## Features

* Automatic irrigation control using soil moisture
* ET-based irrigation recommendation
* Live dashboard visualization
* Comparison of estimated vs actual irrigation

## Methodology

* ET is calculated using temperature and humidity data
* Irrigation requirement = ET − rainfall
* Soil moisture sensor determines actual irrigation duration
* Comparison is made between model and real data

## Hardware

* ESP32 DevKit V1
* Soil moisture sensor
* Relay module

## Software

* Python
* Streamlit
* Arduino IDE

## System Architecture

The system consists of four main components:

1. **ESP32 Sensor Node**

   * Reads soil moisture data
   * Controls irrigation pump using relay
   * Sends data via WiFi

2. **Backend (Python)**

   * Reads live sensor data
   * Processes historical weather data
   * Calculates evapotranspiration (ET)

3. **Data Model**

   * Estimates irrigation requirement using ET
   * Uses temperature, humidity, and rainfall data

4. **Dashboard**

   * Displays live soil moisture
   * Shows irrigation recommendations
   * Compares estimated vs actual irrigation

### Data Flow

ESP32 → Soil Moisture → Python → ET Model → Recommendation → Dashboard


## How to Run

```bash
pip install -r requirements.txt
streamlit run dashboard/streamlit_app.py
```

## Output

* Live soil moisture data
* Irrigation recommendation
* Comparison graph

## Deployment

* HTML dashboard deployed using Netlify (for demo)
* Real-time system runs locally via Python

## Model vs Actual Comparison

The system compares:

* **Estimated Irrigation** (based on ET model)
* **Actual Irrigation** (based on soil moisture sensor)

### Method:

* ET is calculated from historical weather data
* Irrigation requirement = ET − rainfall
* Actual irrigation is determined by the duration between:

  * Pump ON (dry soil)
  * Pump OFF (wet soil)

### Purpose:

This comparison helps evaluate how accurate the model is under real conditions.

## How It Works

1. Soil moisture is continuously monitored using ESP32
2. When soil becomes dry, irrigation is triggered
3. Historical weather data is used to calculate ET
4. The system estimates how much water is needed
5. Actual irrigation is measured using sensor feedback
6. The system compares estimated vs actual irrigation
7. Results are displayed on a dashboard

## Future Work

* Weather API integration
* Mobile app support
* Improved ET modeling

