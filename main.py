from time import sleep
from machine import Pin
from dfplayerpro import DFPlayerPro, UART
from secretgame import SecretGame

# Constants. Change these if DFPlayer is connected to other pins.
UART_INSTANCE = 1
TX_PIN = 7
RX_PIN = 6
GPIO_FROTHER = 3
GPIO_ESPRESSO = 2

# Default volume for all sounds
DEFAULT_VOLUME = 10  # Max 30

# Logging levels
LOG_LEVEL = "INFO"  # Options: "NONE", "ERROR", "WARN", "INFO"


def log(level, message):
    """
    Log a message if the level is equal to or higher than the current LOG_LEVEL.
    """
    levels = {"NONE": -1, "ERROR": 0, "WARN": 1, "INFO": 2}
    if levels[level] <= levels[LOG_LEVEL]:
        print(f"[{level}] {message}")


log("INFO", "Starting up...")


def validate_response(response, success_message, failure_message):
    """
    Validate the response from the DFPlayer and log the appropriate message.

    :param response: The response from the DFPlayer command.
    :param success_message: The message to log if the response is valid.
    :param failure_message: The message to log if the response is invalid.
    :return: True if the response is valid, False otherwise.
    """
    if response and b"OK" in response:
        log("INFO", success_message)
        return True
    else:
        log("WARN", f"{failure_message}: {response}")
        return False


# Create player instance with error handling
try:
    player = DFPlayerPro(UART_INSTANCE, TX_PIN, RX_PIN)
    response = player.test_connection()
    if not validate_response(
        response,
        "DFPlayer connected successfully",
        "DFPlayer not responding or invalid response",
    ):
        player = None  # Set player to None to handle gracefully later
except Exception as e:
    log("ERROR", f"Failed to initialize DFPlayer: {e}")
    player = None

# Disable the prompt tone to stop "music" on startup
if player:
    response = player.set_prompt_tone("OFF")
    validate_response(
        response, "Prompt tone disabled", "Failed to disable prompt tone"
    )

# Configure GPIO_FROTHER and GPIO_ESPRESSO as inputs with pull-up resistors
button_frother = Pin(GPIO_FROTHER, Pin.IN, Pin.PULL_UP)
button_espresso = Pin(GPIO_ESPRESSO, Pin.IN, Pin.PULL_UP)

# Set volume globally
if player:
    response = player.set_volume(DEFAULT_VOLUME)
    validate_response(
        response, f"Volume set to {DEFAULT_VOLUME}", "Failed to set volume"
    )

# Set the filenames to play
FILE_FROTHER = "/01/FROTHER.MP3"  # Frother
FILE_ESPRESSO = "/01/ESPRESSO.MP3"  # Espresso

# Initialize SecretGame
secret_game = SecretGame(player, button_frother, button_espresso, log)

# Main loop
is_playing = False
current_file = None
frother_pressed = False
espresso_pressed = False

try:
    log("INFO", "Entering main loop...")
    while True:
        if player is None:
            log("ERROR", "DFPlayer is not initialized. Exiting loop.")
            break

        if not secret_game.in_game_mode:  # Not in game mode
            if (
                not button_frother.value() and not button_espresso.value()
            ):  # Both buttons pressed
                secret_game.enter_game_mode()
            else:
                # Frother button logic
                if not button_frother.value():  # Frother button pressed
                    if not frother_pressed:
                        frother_pressed = True
                        if not is_playing or current_file != FILE_FROTHER:
                            player.set_volume(
                                DEFAULT_VOLUME
                            )  # Set volume to 10
                            response = player.play_specific_file(FILE_FROTHER)
                            if validate_response(
                                response,
                                f"Playing file {FILE_FROTHER}",
                                f"Failed to play Frother file",
                            ):
                                current_file = player.query_file_name()
                                log(
                                    "INFO",
                                    f"Currently playing file: {current_file}",
                                )
                                is_playing = True
                else:
                    frother_pressed = False

                # Espresso button logic
                if not button_espresso.value():  # Espresso button pressed
                    if not espresso_pressed:
                        espresso_pressed = True
                        if not is_playing or current_file != FILE_ESPRESSO:
                            player.set_volume(
                                DEFAULT_VOLUME
                            )  # Set volume to 10
                            response = player.play_specific_file(FILE_ESPRESSO)
                            if validate_response(
                                response,
                                f"Playing file {FILE_ESPRESSO}",
                                f"Failed to play Espresso file",
                            ):
                                current_file = player.query_file_name()
                                log(
                                    "INFO",
                                    f"Currently playing file: {current_file}",
                                )
                                is_playing = True
                else:
                    espresso_pressed = False

                # Fade-out logic
                if (
                    not frother_pressed and not espresso_pressed
                ):  # No button pressed
                    if is_playing:
                        for vol in range(DEFAULT_VOLUME, -1, -3):
                            player.set_volume(vol)
                            sleep(0.1)
                        response = player.play()
                        if validate_response(
                            response,
                            "Playback stopped",
                            "Failed to stop playback",
                        ):
                            is_playing = False
                            # Reset volume to default after fade-out
                            if player:
                                response = player.set_volume(DEFAULT_VOLUME)
                                validate_response(
                                    response,
                                    f"Volume set to {DEFAULT_VOLUME}",
                                    "Failed to set volume",
                                )
        else:  # In game mode
            secret_game.handle_game_mode()

        sleep(0.1)
except KeyboardInterrupt:
    log("WARN", "KeyboardInterrupt detected, exiting program")
finally:
    if player:
        response = player.send_command(b"AT+STOP")
        validate_response(
            response,
            "Program exited, playback stopped",
            "Failed to send stop command",
        )
