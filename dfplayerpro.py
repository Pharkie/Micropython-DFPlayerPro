from time import ticks_ms, ticks_diff
from machine import UART


class DFPlayerPro:
    COMMAND_COOLDOWN_MS = 500  # Cooldown time 500ms
    RESPONSE_TIMEOUT_MS = 1000  # Timeout for waiting for a response

    def __init__(self, uart_instance, tx_pin, rx_pin):
        """
        Initialize the DFPlayerPro instance.

        :param uart_instance: UART instance number.
        :param tx_pin: TX pin number.
        :param rx_pin: RX pin number.
        """
        self.uart = UART(uart_instance, baudrate=9600, tx=tx_pin, rx=rx_pin)
        self.last_command_time = 0  # Track the last command time

    def _can_send_command(self):
        """
        Check if enough time has passed since the last command was sent.
        """
        current_time = ticks_ms()
        if (
            ticks_diff(current_time, self.last_command_time)
            >= self.COMMAND_COOLDOWN_MS
        ):
            self.last_command_time = current_time
            return True
        return False

    def send_command(self, command):
        """
        Send a command to the DFPlayer with cooldown enforcement.

        :param command: The command to send as bytes.
        :return: True if the command was sent, False otherwise.
        """
        if self._can_send_command():
            self.uart.write(command)
            return True
        else:
            return False  # Command not sent due to cooldown

    def wait_for_response(self):
        """
        Wait for a response from the DFPlayer within the timeout period.

        :return: The response as bytes, or None if no response is received.
        """
        start_time = ticks_ms()
        while ticks_diff(ticks_ms(), start_time) < self.RESPONSE_TIMEOUT_MS:
            response = self.uart.read()
            if response:
                return response
        return None  # Return None if no response is received within the timeout

    def play_specific_file(self, file_path):
        """
        Play a specific file with cooldown enforcement and wait for a response.

        :param file_path: The file path to play as a string.
        :return: The response from the DFPlayer, or None if the command was not sent.
        """
        command = f"AT+PLAYFILE={file_path}\r\n".encode()
        if self.send_command(command):
            return self.wait_for_response()
        return None

    def set_volume(self, volume):
        """
        Set the volume with cooldown enforcement and wait for a response.

        :param volume: The volume level (0-30).
        :return: The response from the DFPlayer, or None if the command was not sent.
        """
        command = f"AT+VOL={volume}\r\n".encode()
        if self.send_command(command):
            return self.wait_for_response()
        return None

    def test_connection(self):
        """
        Test the connection to the DFPlayer and wait for a response.

        :return: The response from the DFPlayer, or None if the command was not sent.
        """
        if self.send_command(b"AT+TEST\r\n"):
            return self.wait_for_response()
        return None

    def set_prompt_tone(self, state):
        """
        Enable or disable the prompt tone with cooldown enforcement and wait for a response.

        :param state: "ON" or "OFF".
        :return: The response from the DFPlayer, or None if the command was not sent.
        """
        command = f"AT+PROMPT={state}\r\n".encode()
        if self.send_command(command):
            return self.wait_for_response()
        return None

    def query_file_name(self):
        """
        Query the currently playing file name with cooldown enforcement and wait for a response.

        :return: The response from the DFPlayer, or None if the command was not sent.
        """
        if self.send_command(b"AT+QUERYFILE\r\n"):
            return self.wait_for_response()
        return None  # Return None if command was not sent due to cooldown
