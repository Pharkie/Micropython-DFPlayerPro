from time import sleep
from dfplayerpro import DFPlayerPro

# Constants. Change these if DFPlayer is connected to other pins.
UART_INSTANCE = 1
TX_PIN = 7
RX_PIN = 6

# Create player instance
player = DFPlayerPro(UART_INSTANCE, TX_PIN, RX_PIN)

# Test connection
# response = player.test_connection()
# print('Connection Test:', response)

# Set volume to a medium level
volume_level = 10
response = player.set_volume(volume_level)
print(f'Volume set to {volume_level}, Response:', response)

# Set the filename to play
filename = '/02/001.mp3'

# Play the specific file
response = player.play_specific_file(filename)
print(f'Playing file {filename}, Response:', response)

sleep(1) # Wait for the file to finish playing

print('Finished')