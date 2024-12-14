import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import numpy as np
from flask import Flask, jsonify, render_template

# Initialize I2C and ADC
i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS.ADS1115(i2c)

# Create analog input channels
chan_soil_moisture1 = AnalogIn(adc, ADS.P2)
chan_tds = AnalogIn(adc, ADS.P0)

# Define window size for Hamming Window
WINDOW_SIZE = 5

# Buffers to store raw sensor readings
buffer_soil_moisture = []
buffer_tds = []

# Function to calculate the Hamming Window
def hamming_window(size):
    return np.hamming(size)

# Function to apply the Hamming Window filter
def apply_hamming_window(buffer, new_value):
    buffer.append(new_value)
    if len(buffer) > WINDOW_SIZE:
        buffer.pop(0)  # Maintain buffer size
    
    # Apply the Hamming window
    weights = hamming_window(len(buffer))
    weighted_values = np.multiply(buffer, weights)
    return np.sum(weighted_values) / np.sum(weights)

# Flask application setup
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Serve the HTML file

@app.route('/data')
def get_data():
    # Read raw values
    soil_moisture_raw = chan_soil_moisture1.value
    tds_raw = chan_tds.value

    # Apply Hamming Window filtering
    filtered_soil_moisture = apply_hamming_window(buffer_soil_moisture, soil_moisture_raw)
    filtered_tds = apply_hamming_window(buffer_tds, tds_raw)

    # Prepare JSON response
    data = {
        "soil_moisture": {
            "raw_value": soil_moisture_raw,
            "filtered_value": round(filtered_soil_moisture, 2)
        },
        "tds": {
            "raw_value": tds_raw,
            "filtered_value": round(filtered_tds, 2)
        }
    }
    return jsonify(data)

# Main loop for Flask and sensor reading
if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Shutting down Flask server...")
