import time
import Adafruit_ADS1x15

# Initialize I2C bus number (usually 1 on Raspberry Pi)
i2c_bus_number = 1

# Create an ADS1115 ADC object
adc = Adafruit_ADS1x15.ADS1115(busnum=i2c_bus_number)

# Set the gain to ±4.096V (adjust if needed)
GAIN = 1

# Main loop to continuously read and display the ADC value
try:
    while True:
        # Read the raw analog value from channel A2
        raw_value = adc.read_adc(2, gain=GAIN)

        # Print the labeled ADC value
        print("Soil Sensor Value: {}".format(raw_value))

        # Add a delay between readings (adjust as needed)
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting...")
