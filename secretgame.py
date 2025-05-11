from time import sleep
import random

# Folder prefix for all file paths
FOLDER_PREFIX = "/02/"

STARTUP_SOUNDS = [
    FOLDER_PREFIX + "ST-DUN.MP3",
    FOLDER_PREFIX + "ST-HORN.MP3",
    FOLDER_PREFIX + "ST-MARIO.MP3",
    FOLDER_PREFIX + "ST-WEAK.MP3",
]

FAIL_SOUNDS = [
    FOLDER_PREFIX + "NO-AWW.MP3",
    FOLDER_PREFIX + "NO-BRASS.MP3",
    FOLDER_PREFIX + "NO-BUZZ.MP3",
    FOLDER_PREFIX + "NO-MARIO.MP3",
    FOLDER_PREFIX + "NO-NOPE.MP3",
    FOLDER_PREFIX + "NO-WEAK.MP3",
]

MYSTERY_SOUNDS = {
    "L": FOLDER_PREFIX + "TM-ALLO.MP3",
    "R": FOLDER_PREFIX + "TM-ATEAM.MP3",
    "LL": FOLDER_PREFIX + "TM-CHRS.MP3",
    "RR": FOLDER_PREFIX + "TM-DRWHO.MP3",
    "LR": FOLDER_PREFIX + "TM-HAWAI.MP3",
    "RL": FOLDER_PREFIX + "TM-HIGN.MP3",
    "LLL": FOLDER_PREFIX + "TM-KNIG.MP3",
    "RRR": FOLDER_PREFIX + "TM-NEIGH.MP3",
    "LRL": FOLDER_PREFIX + "TM-NEV.MP3",
    "RLR": FOLDER_PREFIX + "TM-POSTP.MP3",
    "LLLR": FOLDER_PREFIX + "TM-PRLD.MP3",
    "RRRL": FOLDER_PREFIX + "TM-QUAN.MP3",
    "LRLR": FOLDER_PREFIX + "TM-ROLR.MP3",
    "RLRL": FOLDER_PREFIX + "TM-SPID.MP3",
    "LRRL": FOLDER_PREFIX + "TM-STAR.MP3",
    "RLLR": FOLDER_PREFIX + "TM-STARW.MP3",
    "LLRL": FOLDER_PREFIX + "TM-THOM.MP3",
    "RLRR": FOLDER_PREFIX + "TM-TOPG.MP3",
    "LRLRL": FOLDER_PREFIX + "TM-XFIL.MP3",
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
        self.log("INFO", "Entering game mode")

        startup_sound = random.choice(STARTUP_SOUNDS)
        self.player.play_specific_file(
            startup_sound
        )  # Play random startup sound
        self.sequence = []
        self.in_game_mode = True
        sleep(0.2)  # Debounce delay

    def exit_game_mode(self):
        """
        Exit game mode when both buttons are pressed again.
        """
        self.log("INFO", "Exiting game mode")
        self.in_game_mode = False

    def handle_game_mode(self):
        """
        Handle button presses in game mode.
        """
        if (
            not self.button_left.value() and not self.button_right.value()
        ):  # Both buttons pressed
            self.log("INFO", "Both buttons pressed in game mode")
            self.check_sequence()
            self.exit_game_mode()
            sleep(0.1)  # Debounce delay
        elif not self.button_left.value():  # Left button pressed
            self.log("INFO", "Left button pressed in game mode")
            self.sequence.append("L")
            self.player.play_specific_file(
                FOLDER_PREFIX + "BEEP1.MP3"
            )  # Play beep
            sleep(0.1)  # Debounce delay
        elif not self.button_right.value():  # Right button pressed
            self.log("INFO", "Right button pressed in game mode")
            self.sequence.append("R")
            self.player.play_specific_file(
                FOLDER_PREFIX + "BEEP2.MP3"
            )  # Play boop
            sleep(0.1)  # Debounce delay

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
