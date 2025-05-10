from machine import Pin
import time

# Configure GPIO pins 2 and 3 as inputs with pull-up resistors
gpio2 = Pin(2, Pin.IN, Pin.PULL_UP)
gpio3 = Pin(3, Pin.IN, Pin.PULL_UP)

while True:
    if not gpio2.value():  # Check if GPIO 2 is triggered (active low)
        print("Input detected on GPIO 2")
    if not gpio3.value():  # Check if GPIO 3 is triggered (active low)
        print("Input detected on GPIO 3")
    time.sleep(0.1)  # Small delay to debounce
