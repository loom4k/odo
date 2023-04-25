import RPi.GPIO as GPIO
import time

# Set up the GPIO pins for the ADC
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)

# Define the function to read the ADC value
def read_adc():
    # Read the value from the ADC
    adc_value = 0
    for i in range(10):
        adc_value += GPIO.input(7)
        time.sleep(0.001)
    adc_value = adc_value / 10

    # Convert the ADC value to a voltage (0-3.3V)
    voltage = adc_value * (3.3 / 1023)

    # Convert the voltage to a value between 0 and 100
    value = int((voltage / 3.3) * 100)

    return value

# Main program loop
while True:
    # Read the ADC value
    adc_value = read_adc()

    # Print the value to the console
    print("Potentiometer value: {}".format(adc_value))

    # Wait for a short time before reading again
    time.sleep(0.1)
