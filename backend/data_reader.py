import serial
import time

# CONFIGURATION
PORT = 'COM3' 
BAUD_RATE = 115200 # Must match Serial.begin() in Arduino code

try:
    # Open the connection
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(2) # Give the ESP32 time to reset
    print(f"Connected to ESP32 on {PORT}")

    while True:
        if ser.in_waiting > 0:
            # Read the line of data from the ESP32
            line = ser.readline().decode('utf-8').strip()
            print(f"Incoming Data: {line}")
            
except serial.SerialException as e:
    print(f"Error: Could not open port {PORT}. Check if the Serial Monitor in Arduino IDE is still open!")
except KeyboardInterrupt:
    print("Stopping the listener...")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
