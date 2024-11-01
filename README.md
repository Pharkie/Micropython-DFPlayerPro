# DFPlayer Pro MicroPython Library

This library is a MicroPython implementation for controlling the DFPlayer Pro MP3 Player module. It uses AT commands over UART, based on the data sheet provided by DFRobot. Tested with an ESP32-C3 Super mini.

## Features

- Set volume level
- Play specific files
- Control playback (play, pause, next, previous)
- Query current playback status
- Set playback modes
- Fast forward and rewind

## DFPlayerPro Data Sheet

Refer to the [DFPlayerPro Data Sheet](https://dfimg.dfrobot.com/nobody/wiki/a6ec053c2390018d801e2ed31f0c6329.pdf).

## Requirements

- MicroPython-compatible board (e.g., ESP32-C3)
- DFPlayer Pro MP3 Player module. Not the DFPlayer Mini, because it uses entirely different serial commands.
- UART connection between the board and the DFPlayer Pro

## Hardware Setup

1. **Connect the DFPlayer Pro to the MicroPython board**:
    - **TX Pin** on DFPlayer Pro to **RX Pin** on the MicroPython board.
    - **RX Pin** on DFPlayer Pro to **TX Pin** on the MicroPython board.
    - **GND** on DFPlayer Pro to **GND** on the MicroPython board or shared from the power supply.
    - **VCC** on DFPlayer Pro to **3.3V** on the MicroPython board.

## Installation

1. Clone this repository to your local machine.
2. Copy the files to your MicroPython board.

## DFPlayerPro Class Methods

- `test_connection()`: Test the connection to the DFPlayer Pro by sending a simple AT command.
- `set_volume(volume_level)`: Set the volume level of the DFPlayer Pro (0-30).
- `query_volume()`: Query the current volume level of the DFPlayer Pro.
- `set_play_mode(mode)`: Set the playback mode of the DFPlayer Pro.
- `query_play_mode()`: Query the current playback mode of the DFPlayer Pro.
- `play_specific_file(file_path)`: Play a specific file on the DFPlayer Pro.
- `play()`: Toggle play/pause on the DFPlayer Pro.
- `next_track()`: Play the next track on the DFPlayer Pro.
- `previous_track()`: Play the previous track on the DFPlayer Pro.
- `fast_rewind(seconds)`: Fast rewind the current track by a specified number of seconds.
- `fast_forward(seconds)`: Fast forward the current track by a specified number of seconds.
- `play_from_second(second)`: Start playing the current track from a specified second.
- `query_current_track()`: Query the file number of the currently playing track.
- `query_total_files()`: Query the total number of files on the DFPlayer Pro.
- `query_played_time()`: Query the time length the current track has played.
- `query_total_time()`: Query the total time of the currently playing track.
- `query_file_name()`: Query the file name of the currently playing track.
- `play_file_number(file_number)`: Play a specific file by its number.
- `delete_current_file()`: Delete the currently playing file.
- `set_amplifier(state)`: Turn the amplifier on or off.
- `record()`: Start or pause recording.
- `save_recording()`: Save the recorded voice.
- `set_baud_rate(baud_rate)`: Set the baud rate for UART communication.
- `set_prompt_tone(state)`: Turn the prompt tone on or off.
- `set_led(state)`: Turn the LED prompt on or off.

## Troubleshooting

- **No Response from DFPlayer Pro**: Ensure the TX and RX pins are correctly connected and the baud rate is set to 115200.
- **File Not Playing**: Verify the file path and ensure the file exists on the DFPlayer Pro.
- **Volume Not Changing**: Ensure the volume level is within the range of 0-15.

## Contributing

Contributions are welcome! Please fork this repository and submit a pull request with your changes. I'm not good at Git, but I'll see if I can figure out how to incorporate.

## License
This project is licensed under the MIT License.

## Example

See `dfplayerpro_example.py`