import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
os.system('cls' if os.name == 'nt' else 'clear')

# 1. Configuration
file_path = r'C:\Users\User\Downloads\Daily_Weather_Summary.csv' # Use your copied path
LATITUDE = 12.12  # Your latitude
ELEVATION = 1     # Your elevation in meters

df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'])

def get_refined_et(row):
    # Extract weather variables
    t_max, t_min = row['Tmax (degC)'], row['Tmin (degC)']
    t_mean = row['Tmean (degC)']
    rh = row['Humidity Mean (%)']
    u2 = row['Wind Speed Mean (m/s)']
    rs = row['Radiation (MJ/m2/day)']
    
    # Day of year for radiation math
    doy = row['Date'].timetuple().tm_yday
    
    # 1. Psychrometric constant & Delta
    p = 101.3 * ((293 - 0.0065 * ELEVATION) / 293)**5.26
    gamma = 0.000665 * p
    delta = (4098 * (0.6108 * np.exp((17.27 * t_mean) / (t_mean + 237.3)))) / (t_mean + 237.3)**2
    
    # 2. Vapor Pressure Deficit
    es = (0.6108 * np.exp((17.27 * t_max) / (t_max + 237.3)) + 
          0.6108 * np.exp((17.27 * t_min) / (t_min + 237.3))) / 2
    ea = (rh / 100) * es
    vpd = es - ea

    # 3. Net Radiation (Simplified Rn for Tomatoes)
    # 0.77 is the standard albedo for green crops
    rn = 0.77 * rs 

    # 4. FAO-56 Penman-Monteith Equation
    eto = (0.408 * delta * rn + gamma * (900 / (t_mean + 273)) * u2 * vpd) / (delta + gamma * (1 + 0.34 * u2))
    return eto

# Calculate and Compare
df['ETo_Refined'] = df.apply(get_refined_et, axis=1)


# 1. Calculate ETc (Crop ET) using the Kc column already in your file
df['ETc_Refined'] = df['ETo_Refined'] * df['Kc']

# 2. Define the name of your new file
output_filename = 'Refined_Tomato_Irrigation_Data.csv'

# 3. Save to CSV
# index=False prevents Python from adding an extra column of numbers (0, 1, 2...)
df.to_csv("New_Weather", index=False)

print(f"Successfully saved refined data to: {'New_Weather'}")

# VISUALIZATION
plt.figure(figsize=(10, 5))

plt.plot(df['Date'], df['ETc_Refined'], color='darkgreen', label='ETc (Crop Water Demand)')

plt.title(f'Irrigation Demand For Tomato Based on ETc (Lat: {LATITUDE}N)')
plt.ylabel('ETc in mm/day')
plt.xlabel('Crop cycle: Nov 2025 - Feb 2026')
plt.legend()
plt.savefig('Irrigation_Graph.png')
print("Graph saved as image")

