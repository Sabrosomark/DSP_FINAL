import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C and ADC
i2c = busio.I2C(board.SCL, board.SDA)
adc = ADS.ADS1115(i2c)

# Create analog input channels
chan_soil_moisture1 = AnalogIn(adc, ADS.P2)
chan_tds = AnalogIn(adc, ADS.P0)

# Function to display raw values
def display_raw_values():
    soil_moisture_raw = chan_soil_moisture1.value
    tds_raw = chan_tds.value
    
    print(f"Soil Moisture Raw Value: {soil_moisture_raw}")
    print(f"TDS Raw Value: {tds_raw}")

# Main loop to continuously display raw values
while True:
    display_raw_values()
    time.sleep(1)  # Delay to avoid overwhelming the output
