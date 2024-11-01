from machine import UART, Pin
from utime import sleep_ms

# Constants. Change these if DFPlayer is connected to other pins.
UART_INSTANCE = 1
TX_PIN = 7
RX_PIN = 6
BAUD_RATE = 115200

# Initialize UART
print(f"Initializing UART{UART_INSTANCE} with TX pin {TX_PIN} " +
      f"and RX pin {RX_PIN} at {BAUD_RATE} baud rate.")
uart = UART(UART_INSTANCE, baudrate=BAUD_RATE, tx=Pin(TX_PIN), rx=Pin(RX_PIN))
print("UART initialized.")

# Function to send a command and print the response
def send_command(command):
    print(f"Sending command: {command}")
    uart.write(command + b'\r\n')
    sleep_ms(500)  # Wait for the response
    response = uart.read()
    print(f"Sent: {command}, Received: {response}")
    return response

# Test connection with a simple AT command
print("Testing connection with AT command.")
response = send_command(b"AT")
print(f"Connection Test Response: {response}")

# Can add more commands to test
# print("Querying volume.")
# response = send_command(b"AT+VOL=?")
# print(f"Volume Query Response: {response}")
