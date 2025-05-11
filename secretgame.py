from time import sleep
import random

STARTUP_SOUNDS = [
    "ST-DUN.MP3",
    "ST-HORN.MP3",
    "ST-MARIO.MP3",
    "ST-WEAK.MP3",
]

FAIL_SOUNDS = [
    "NO-AWW.MP3",
    "NO-BRASS.MP3",
    "NO-BUZZ.MP3",
    "NO-MARIO.MP3",
    "NO-NOPE.MP3",
    "NO-WEAK.MP3",
]

MYSTERY_SOUNDS = {
    "LRLL": "TM-ALLO.MP3",
    "RR": "TM-ATEAM.MP3",
    "LLR": "TM-CHRS.MP3",
    "RRL": "TM-DRWHO.MP3",
    "LRR": "TM-HAWAI.MP3",
    "RLL": "TM-HIGN.MP3",
    "LL": "TM-KNIG.MP3",
    "RL": "TM-NEIGH.MP3",
    "LR": "TM-NEV.MP3",
    "RRLL": "TM-POSTP.MP3",
    "LLRR": "TM-PRLD.MP3",
    "LRLR": "TM-QUAN.MP3",
    "RLRL": "TM-ROLR.MP3",
    "LRRL": "TM-SPID.MP3",
    "RLLR": "TM-STAR.MP3",
    "RRLR": "TM-STARW.MP3",
    "LLRL": "TM-THOM.MP3",
    "RLRR": "TM-TOPG.MP3",
    "LRLRL": "TM-XFIL.MP3",
}


class SecretGame:
    def __init__(self, player, button_left, button_right, log_func):
        """
        Initialize the SecretGame class.

        :param player: DFPlayerPro instance for playing sounds.
        :param button_left: Pin instance for the left button.
        :param button_right: Pin instance for the right button.
        :param log_func: Logging function for debug output.
        """
        self.player = player
        self.button_left = button_left
        self.button_right = button_right
        self.log = log_func
        self.sequence = []
        self.in_game_mode = False

    def enter_game_mode(self):
        """
        Enter game mode when both buttons are pressed simultaneously.
        """
        self.log("INFO", "Entering game mode, advanced")
        startup_sound = random.choice(STARTUP_SOUNDS)
        self.player.play_specific_file(
            startup_sound
        )  # Play random startup sound
        self.sequence = []
        self.in_game_mode = True
        sleep(1)  # Debounce delay

    def handle_game_mode(self):
        """
        Handle button presses in game mode.
        """
        if (
            not self.button_left.value() and not self.button_right.value()
        ):  # Both buttons pressed
            self.log("INFO", "Both buttons pressed in game mode")
            self.check_sequence()
            self.in_game_mode = False
            sleep(1)  # Debounce delay
        elif not self.button_left.value():  # Left button pressed
            self.log("INFO", "Left button pressed in game mode")
            self.sequence.append("L")
            self.player.play_specific_file("02/002.mp3")  # Play beep
            sleep(0.5)  # Debounce delay
        elif not self.button_right.value():  # Right button pressed
            self.log("INFO", "Right button pressed in game mode")
            self.sequence.append("R")
            self.player.play_specific_file("02/003.mp3")  # Play boop
            sleep(0.5)  # Debounce delay

    def check_sequence(self):
        """
        Check the collected sequence against the MYSTERY_SOUNDS dictionary.
        """
        sequence_str = "".join(self.sequence)
        self.log("INFO", f"Checking sequence: {sequence_str}")
        if sequence_str in MYSTERY_SOUNDS:
            self.log("INFO", f"Sequence matched: {sequence_str}")
            self.player.play_specific_file(
                MYSTERY_SOUNDS[sequence_str]
            )  # Play success sound
        else:
            self.log("WARN", f"Sequence not matched: {sequence_str}")
            fail_sound = random.choice(FAIL_SOUNDS)
            self.player.play_specific_file(fail_sound)  # Play random fail sound
