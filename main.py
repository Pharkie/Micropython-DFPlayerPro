from time import sleep
from machine import Pin
from dfplayerpro import DFPlayerPro
from secretgame import SecretGame

# Constants. Change these if DFPlayer is connected to other pins.
UART_INSTANCE = 1
TX_PIN = 7
RX_PIN = 6
GPIO2 = 2
GPIO3 = 3

# Logging levels
LOG_LEVEL = "INFO"  # Options: "NONE", "ERROR", "WARN", "INFO"


def log(level, message):
    """
    Log a message if the level is equal to or higher than the current LOG_LEVEL.
    """
    levels = {"NONE": -1, "ERROR": 0, "WARN": 1, "INFO": 2}
    if levels[level] <= levels[LOG_LEVEL]:
        print(f"[{level}] {message}")


# Create player instance
player = DFPlayerPro(UART_INSTANCE, TX_PIN, RX_PIN)

# Disable the prompt tone to stop "music" on startup
response = player.set_prompt_tone("OFF")
log("INFO", f"Prompt tone disabled, Response: {response}")

# Configure GPIO2 and GPIO3 as inputs with pull-up resistors
button_frother = Pin(GPIO3, Pin.IN, Pin.PULL_UP)
button_espresso = Pin(GPIO2, Pin.IN, Pin.PULL_UP)

# Set volume to a medium level
volume_level = 10  # Max 30
response = player.set_volume(volume_level)
log("INFO", f"Volume set to {volume_level}, Response: {response}")

# Set the filenames to play
file_frother = "/01/FROTHER.MP3"  # Frother
file_espresso = "/01/ESPRESSO.MP3"  # Espresso

# Initialize SecretGame
secret_game = SecretGame(player, button_frother, button_espresso, log)

# Main loop
is_playing = False
has_faded_out = False
current_file = None
frother_pressed = False
espresso_pressed = False

try:
    while True:
        if not secret_game.in_game_mode:  # Not in game mode
            if (
                not button_frother.value() and not button_espresso.value()
            ):  # Both buttons pressed
                secret_game.enter_game_mode()
            else:
                # Existing button logic
                if not button_frother.value():  # Frother button pressed
                    if not frother_pressed:
                        frother_pressed = True
                        if (
                            not is_playing
                            or has_faded_out
                            or current_file != file_frother
                        ):
                            response = player.play_specific_file(file_frother)
                            log(
                                "INFO",
                                f"Playing file {file_frother}, Response: {response}",
                            )
                            current_file = player.query_file_name()
                            log(
                                "INFO",
                                f"Currently playing file: {current_file}",
                            )
                            player.set_volume(volume_level)
                            is_playing = True
                            has_faded_out = False
                else:
                    frother_pressed = False

                if not button_espresso.value():  # Espresso button pressed
                    if not espresso_pressed:
                        espresso_pressed = True
                        if (
                            not is_playing
                            or has_faded_out
                            or current_file != file_espresso
                        ):
                            response = player.play_specific_file(file_espresso)
                            log(
                                "INFO",
                                f"Playing file {file_espresso}, Response: {response}",
                            )
                            current_file = player.query_file_name()
                            log(
                                "INFO",
                                f"Currently playing file: {current_file}",
                            )
                            player.set_volume(volume_level)
                            is_playing = True
                            has_faded_out = False
                else:
                    espresso_pressed = False

                if (
                    not frother_pressed and not espresso_pressed
                ):  # No button pressed
                    if is_playing:
                        for vol in range(volume_level, -1, -3):
                            if (
                                not button_frother.value()
                                or not button_espresso.value()
                            ):
                                player.set_volume(volume_level)
                                log(
                                    "INFO",
                                    "Button re-pressed, restoring volume",
                                )
                                break
                            player.set_volume(vol)
                            sleep(0.1)
                        else:
                            response = player.play()
                            log("INFO", "Playback stopped")
                            is_playing = False
                            has_faded_out = True
        else:  # In game mode
            secret_game.handle_game_mode()

        sleep(0.1)
except KeyboardInterrupt:
    log("WARN", "KeyboardInterrupt detected, exiting program")
finally:
    player.send_command(b"AT+STOP")
    log("INFO", "Program exited, playback stopped.")
