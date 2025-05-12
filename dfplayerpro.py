from time import ticks_ms, ticks_diff, sleep
from machine import UART


class DFPlayerPro:
    RESPONSE_TIMEOUT_MS = 1000  # Timeout for waiting for a response
    LOG_LEVEL = (
        "INFO"  # Default log level: "NONE", "ERROR", "WARN", "INFO", "DEBUG"
    )

    def __init__(self, uart_instance, tx_pin, rx_pin, log_level="INFO"):
        """
        Initialize the DFPlayerPro instance.

        :param uart_instance: UART instance number.
        :param tx_pin: TX pin number.
        :param rx_pin: RX pin number.
        :param log_level: Log level as a string ("NONE", "ERROR", "WARN", "INFO", "DEBUG").
        """
        self.uart = UART(uart_instance, baudrate=115200, tx=tx_pin, rx=rx_pin)
        self.LOG_LEVEL = log_level  # Set the log level

    def _log(self, level, message):
        """
        Internal logging function for the DFPlayerPro class.

        :param level: Log level as a string ("NONE", "ERROR", "WARN", "INFO", "DEBUG").
        :param message: The message to log.
        """
        levels = {"NONE": -1, "ERROR": 0, "WARN": 1, "INFO": 2, "DEBUG": 3}
        if levels[level] <= levels[self.LOG_LEVEL]:
            print(f"[{level}] {message}")

    def send_command(self, command):
        """
        Send a command to the DFPlayer and wait for a response.

        :param command: The command to send as bytes.
        :return: The response from the DFPlayer, or None if no response is received.
        """
        self.uart.write(command)
        self._log("DEBUG", f"Command sent: {command}")
        response = self.wait_for_response()  # Wait for and return the response
        sleep(0.1)  # Small delay to allow for processing
        return response

    def wait_for_response(self):
        """
        Wait for a response from the DFPlayer within the timeout period.

        :return: The full response as bytes, or None if no response is received.
        """
        start_time = ticks_ms()
        response = b""  # Initialize an empty response buffer
        while ticks_diff(ticks_ms(), start_time) < self.RESPONSE_TIMEOUT_MS:
            chunk = self.uart.read()  # Read a chunk of data from UART
            if chunk:
                response += chunk  # Append the chunk to the response buffer
                self._log("DEBUG", f"Received chunk: {chunk}")
                if response.endswith(
                    b"\r\n"
                ):  # Check if the response is complete
                    self._log("DEBUG", f"Full response: {response}")
                    return response
        self._log("DEBUG", "No complete response received within timeout")
        return None  # Return None if no complete response is received

    def play_specific_file(self, file_path):
        """
        Play a specific file.

        :param file_path: The file path to play as a string.
        :return: The response from the DFPlayer, or None if the command was not sent.
        """
        command = f"AT+PLAYFILE={file_path}\r\n".encode()
        return self.send_command(command)

    def set_volume(self, volume):
        """
        Set the volume.

        :param volume: The volume level (0-30).
        :return: The response from the DFPlayer, or None if the command was not sent.
        """
        command = f"AT+VOL={volume}\r\n".encode()
        return self.send_command(command)

    def test_connection(self):
        """
        Test the connection to the DFPlayer using the AT command.

        :return: The response from the DFPlayer, or None if no response is received.
        """
        return self.send_command(b"AT\r\n")

    def set_prompt_tone(self, state):
        """
        Enable or disable the prompt tone.

        :param state: "ON" or "OFF".
        :return: The response from the DFPlayer, or None if the command was not sent.
        """
        command = f"AT+PROMPT={state}\r\n".encode()
        return self.send_command(command)

    def query_file_name(self):
        """
        Query the currently playing file name.

        :return: The file name as a decoded string, or None if the command was not sent or the response is invalid.
        """
        response = self.send_command(b"AT+QUERY=5\r\n")  # Query file name
        if response and b"\r\n" in response:  # Validate the response format
            try:
                decoded_name = response.strip().decode(
                    "utf-16", errors="ignore"
                )
                self._log("INFO", f"Queried file name: {decoded_name}")
                return decoded_name
            except Exception as e:
                self._log(
                    "WARN",
                    f"Failed to decode file name: {response}, Error: {e}",
                )
        else:
            self._log(
                "WARN", f"Invalid response for query_file_name: {response}"
            )
        return None

    def play_next(self):
        """
        Play the next track.

        :return: The response from the DFPlayer, or None if the command was not sent.
        """
        return self.send_command(b"AT+PLAY=NEXT\r\n")

    def play_previous(self):
        """
        Play the previous track.

        :return: The response from the DFPlayer, or None if the command was not sent.
        """
        return self.send_command(b"AT+PLAY=LAST\r\n")
