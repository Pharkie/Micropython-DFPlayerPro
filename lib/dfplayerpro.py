# Description: This library is a MicroPython implementation of the
# DFPlayer Pro MP3 Player module. It is based on the data sheet provided
# by the manufacturer.
# The library was tested with an ESP32-C3 Super mini.
# Author: Adam Knowles
# Date: 2024-11-01
# License: MIT

from machine import UART, Pin
from utime import sleep_ms


class DFPlayerPro:
    """
    A class to control the DFPlayer Pro MP3 Player module using AT commands over UART.
    """

    UART_BAUD_RATE = 115200  # Default baud rate as per the data sheet
    UART_BITS = 8
    UART_PARITY = None
    UART_STOP = 1
    COMMAND_LATENCY = 200

    def __init__(self, uart_instance, tx_pin, rx_pin):
        """
        Initialize the DFPlayer Pro with the specified UART instance and pins.

        :param uart_instance: The UART instance number (e.g., 1 for UART1).
        :param tx_pin: The GPIO pin number for UART TX.
        :param rx_pin: The GPIO pin number for UART RX.
        """
        self.uart = UART(
            uart_instance,
            baudrate=self.UART_BAUD_RATE,
            tx=Pin(tx_pin),
            rx=Pin(rx_pin),
            bits=self.UART_BITS,
            parity=self.UART_PARITY,
            stop=self.UART_STOP,
        )

    def send_command(self, command):
        """
        Send an AT command to the DFPlayer Pro and return the response.

        :param command: The AT command to send (as a byte string).
        :return: The response from the DFPlayer Pro (as a byte string).
        """
        self.uart.write(command + b"\r\n")
        sleep_ms(self.COMMAND_LATENCY)
        response = self.uart.read()
        # print(f"Sent: {command}, Received: {response}")
        return response

    def test_connection(self):
        """
        Test the connection to the DFPlayer Pro by sending a simple AT command.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT")

    def set_volume(self, volume_level):
        """
        Set the volume level of the DFPlayer Pro.

        :param volume_level: The volume level (0-30).
        :return: The response from the DFPlayer Pro.
        """
        command = f"AT+VOL={volume_level}".encode()
        return self.send_command(command)

    def query_volume(self):
        """
        Query the current volume level of the DFPlayer Pro.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+VOL=?")

    def set_play_mode(self, mode):
        """
        Set the playback mode of the DFPlayer Pro.

        :param mode: The playback mode (1: repeat one song, 2: repeat all, 3: play one song and pause, 4: play randomly, 5: repeat all in the folder).
        :return: The response from the DFPlayer Pro.
        """
        command = f"AT+PLAYMODE={mode}".encode()
        return self.send_command(command)

    def query_play_mode(self):
        """
        Query the current playback mode of the DFPlayer Pro.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+PLAYMODE=?")

    def play_specific_file(self, file_path):
        """
        Play a specific file on the DFPlayer Pro.

        :param file_path: The path to the file to play (e.g., '/01/001.mp3').
        :return: The response from the DFPlayer Pro.
        """
        command = f"AT+PLAYFILE={file_path}".encode()
        return self.send_command(command)

    def play(self):
        """
        Toggle play/pause on the DFPlayer Pro.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+PLAY=PP")

    def next_track(self):
        """
        Play the next track on the DFPlayer Pro.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+PLAY=NEXT")

    def previous_track(self):
        """
        Play the previous track on the DFPlayer Pro.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+PLAY=LAST")

    def fast_rewind(self, seconds):
        """
        Fast rewind the current track by a specified number of seconds.

        :param seconds: The number of seconds to rewind.
        :return: The response from the DFPlayer Pro.
        """
        command = f"AT+TIME=-{seconds}".encode()
        return self.send_command(command)

    def fast_forward(self, seconds):
        """
        Fast forward the current track by a specified number of seconds.

        :param seconds: The number of seconds to fast forward.
        :return: The response from the DFPlayer Pro.
        """
        command = f"AT+TIME=+{seconds}".encode()
        return self.send_command(command)

    def play_from_second(self, second):
        """
        Start playing the current track from a specified second.

        :param second: The second to start playing from.
        :return: The response from the DFPlayer Pro.
        """
        command = f"AT+TIME={second}".encode()
        return self.send_command(command)

    def query_current_track(self):
        """
        Query the file number of the currently playing track.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+QUERY=1")

    def query_total_files(self):
        """
        Query the total number of files on the DFPlayer Pro.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+QUERY=2")

    def query_played_time(self):
        """
        Query the time length the current track has played.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+QUERY=3")

    def query_total_time(self):
        """
        Query the total time of the currently playing track.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+QUERY=4")

    def query_file_name(self):
        """
        Query the file name of the currently playing track.

        :return: The file name of the currently playing track (decoded and cleaned).
        """
        response = self.send_command(b"AT+QUERY=5")
        if response:
            try:
                # Decode the response from UTF-16 and strip unnecessary parts
                decoded_response = response.decode("utf-16").strip("OK\r\n")
                return decoded_response
            except UnicodeDecodeError:
                return "Error decoding response"
        return "No response received"

    def play_file_number(self, file_number):
        """
        Play a specific file by its number.

        :param file_number: The file number to play.
        :return: The response from the DFPlayer Pro.
        """
        command = f"AT+PLAYNUM={file_number}".encode()
        return self.send_command(command)

    def delete_current_file(self):
        """
        Delete the currently playing file.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+DEL")

    def set_amplifier(self, state):
        """
        Turn the amplifier on or off.

        :param state: The state of the amplifier ('ON' or 'OFF').
        :return: The response from the DFPlayer Pro.
        """
        command = f"AT+AMP={state}".encode()
        return self.send_command(command)

    def record(self):
        """
        Start or pause recording.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+REC=RP")

    def save_recording(self):
        """
        Save the recorded voice.

        :return: The response from the DFPlayer Pro.
        """
        return self.send_command(b"AT+REC=SAVE")

    def set_baud_rate(self, baud_rate):
        """
        Set the baud rate for UART communication.

        :param baud_rate: The baud rate to set (e.g., 9600, 19200, 38400, 57600, 115200).
        :return: The response from the DFPlayer Pro.
        """
        command = f"AT+BAUDRATE={baud_rate}".encode()
        return self.send_command(command)

    def set_prompt_tone(self, state):
        """
        Turn the prompt tone on or off.

        :param state: The state of the prompt tone ('ON' or 'OFF').
        :return: The response from the DFPlayer Pro.
        """
        command = f"AT+PROMPT={state}".encode()
        return self.send_command(command)

    def set_led(self, state):
        """
        Turn the LED prompt on or off.

        :param state: The state of the LED prompt ('ON' or 'OFF').
        :return: The response from the DFPlayer Pro.
        """
        command = f"AT+LED={state}".encode()
        return self.send_command(command)


# Example usage
# dfplayer = DFPlayerPro(uart_instance=1, tx_pin=21, rx_pin=20)
# dfplayer.test_connection()
# dfplayer.set_volume(15)
# dfplayer.play_specific_file('/01/001.mp3')
