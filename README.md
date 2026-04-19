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

## Future Work

* Weather API integration
* Mobile app support
* Improved ET modeling

