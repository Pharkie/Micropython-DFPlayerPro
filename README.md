# DFPlayer Pro MicroPython library, and the toy coffee machine that uses it

A MicroPython library for the [DFRobot DFPlayer Pro](https://wiki.dfrobot.com/DFPlayer_PRO_SKU_DFR0768) MP3 module (AT commands over UART), plus the code that runs the sound in my build of the [Cafe Nora toy espresso machine](https://makerworld.com/en/models/858336-cafe-nora-a-toy-espresso-machine-grinder) on MakerWorld. The matching grinder remix is [here](https://makerworld.com/en/models/938277-toy-coffee-grinder-now-usb-c-rechargeable).

The original Cafe Nora design uses a DY sound board that needs 6V. This version swaps that for an ESP32 and a DFPlayer Pro, which both run on 3.3-5V, so the whole machine runs from a single 3.7V LiPo and charges over USB-C.

## What's in this repo

| File | What it is |
| --- | --- |
| `main.py` | The coffee machine program. Runs on boot. Two levers play the espresso and frother sounds. |
| `secretgame.py` | Hidden mode: hold both levers to enter, then tap a left/right sequence to play a TV theme tune. |
| `dfplayerpro.py` | Trimmed DFPlayer Pro driver used by `main.py`. Waits for a proper `\r\n` response to each command, which made it more reliable than the full library. |
| `lib/dfplayerpro.py` | The full library with every AT command wrapped (see method list below). |
| `lib/picodfplayer_mini.py` | A DFPlayer Mini driver. Not used by the coffee machine; the Mini speaks a different protocol. |
| `examples/` | Small standalone scripts: play one file, serial test, DFPlayer Mini test. |
| `buttontest.py` | Prints when each lever is pressed. Useful for checking wiring before anything else. |

## Coffee machine build

### Parts

- ESP32-C3 Super Mini (any MicroPython-capable ESP32 will do, but the pin numbers below are for the C3 Super Mini)
- DFPlayer Pro (DFR0768). Not the DFPlayer Mini: different commands, and it needs a microSD card
- Small speaker, 8 ohm, up to 3W. The 52mm speaker from the original BOM is fine
- 3.7V LiPo with built-in protection, plus a USB-C LiPo charger board
- The two 7x7mm tactile switches from the original design, one under each lever

### Wiring

| ESP32-C3 Super Mini | Connects to | Notes |
| --- | --- | --- |
| GPIO 7 (TX) | DFPlayer Pro RX | UART 1 |
| GPIO 6 (RX) | DFPlayer Pro TX | UART 1 |
| 3.3V | DFPlayer Pro VIN | |
| GND | DFPlayer Pro GND | Shared ground |
| GPIO 2 | Espresso lever switch | Other leg of the switch to GND |
| GPIO 3 | Frother lever switch | Other leg of the switch to GND |

- The speaker goes on the DFPlayer Pro's speaker output pins.
- The switches need no resistors. `main.py` turns on the ESP32's internal pull-ups, so a pressed switch reads low.
- Power: the LiPo, via the charger board, feeds the ESP32's 5V pin. The board's own regulator makes the 3.3V for the DFPlayer Pro.

Change the pin numbers at the top of `main.py` if you wire it differently.

### MP3 files on the DFPlayer Pro

Plug the DFPlayer Pro into a computer over USB-C and it shows up as a USB drive. Make two folders in the root and copy the files in. Keep the names short (8.3 style, upper case) and use the exact names below, because the code refers to them by name.

```
/01/ESPRESSO.MP3   played while the espresso lever is held
/01/FROTHER.MP3    played while the frother lever is held
/02/ST-MARIO.MP3   secret game: startup sound
/02/NO-MARIO.MP3   secret game: fail sound
/02/BEEP1.MP3      secret game: left lever tap
/02/BEEP2.MP3      secret game: right lever tap
/02/TM-*.MP3       secret game: one theme tune per sequence, see secretgame.py
```

The espresso and frother sounds came from the free files linked in the original Cafe Nora listing. The theme tunes are not included here for licence reasons; use your own.

### How it works

- Hold a lever and its sound plays. Let go and it fades out over about half a second.
- Hold both levers at once to enter the secret game. It plays the startup sound, then each lever tap plays a beep and adds an L or R to a sequence. Press both levers again to check the sequence. A match plays that tune. A mismatch, or more than four taps, plays the fail sound and drops back to normal mode.

The sequence-to-tune table is `MYSTERY_SOUNDS` in `secretgame.py`. Edit it to change the tunes or the codes.

### Adding your own songs on buttons

1. Copy the MP3s onto the DFPlayer Pro, for example into a new `/03/` folder.
2. Wire each push button between a spare GPIO and GND.
3. In `main.py`, add a `Pin(<gpio>, Pin.IN, Pin.PULL_UP)` for the button, then copy one of the two lever blocks in the main loop and change the file path to your song. The lever blocks stop the sound when you let go; delete the fade-out part if you want the song to play through.

### Installing

1. Flash MicroPython onto the ESP32. [Thonny](https://thonny.org/) can do this from its Tools > Options > Interpreter dialog, or use `esptool` with the [ESP32-C3 firmware](https://micropython.org/download/ESP32_GENERIC_C3/).
2. Copy `main.py`, `secretgame.py` and `dfplayerpro.py` to the root of the board (Thonny: right-click the file, Upload to /).
3. Reset the board. `main.py` runs automatically. Open the serial console in Thonny to see the log; set `LOG_LEVEL` in `main.py` to `"INFO"` once it's working.

## DFPlayer Pro library

This is `lib/dfplayerpro.py`, the full library. Tested with an ESP32-C3 Super Mini.

### Features

- Set volume level
- Play specific files
- Control playback (play, pause, next, previous)
- Query current playback status
- Set playback modes
- Fast forward and rewind

### DFPlayerPro data sheet

Refer to the [DFPlayer Pro data sheet](https://dfimg.dfrobot.com/nobody/wiki/a6ec053c2390018d801e2ed31f0c6329.pdf).

### Requirements

- MicroPython-compatible board (e.g. ESP32-C3)
- DFPlayer Pro MP3 player module. Not the DFPlayer Mini, because it uses entirely different serial commands
- UART connection between the board and the DFPlayer Pro

### Hardware setup

Connect the DFPlayer Pro to the MicroPython board:

- **TX pin** on DFPlayer Pro to **RX pin** on the MicroPython board
- **RX pin** on DFPlayer Pro to **TX pin** on the MicroPython board
- **GND** on DFPlayer Pro to **GND** on the MicroPython board, or shared from the power supply
- **VCC** on DFPlayer Pro to **3.3V** on the MicroPython board

### DFPlayerPro class methods

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

### Example

See `examples/dfplayerpro_example.py`.

## Troubleshooting

- **No response from DFPlayer Pro**: Check TX and RX are crossed over (TX to RX, RX to TX) and the baud rate is 115200. `examples/serial_test.py` sends a bare `AT` and prints whatever comes back.
- **Levers do nothing**: Run `buttontest.py`. If it prints nothing when you press a lever, the switch is wired to the wrong pin or not to GND.
- **File not playing**: The path must match the file on the DFPlayer Pro exactly, including the folder and the `.MP3` extension.
- **Volume not changing**: The level must be within 0-30.
- **Music plays on power-up**: That is the DFPlayer Pro's prompt tone. `main.py` turns it off with `set_prompt_tone("OFF")`.

## Contributing

Contributions are welcome. Please fork this repository and submit a pull request with your changes. I'm not good at Git, but I'll see if I can figure out how to incorporate.

## License

MIT.
