from time import sleep

# Folder prefix for all file paths
FOLDER_PREFIX = "/02/"

# Debounce delay for button presses
DEBOUNCE_DELAY = 0.3  # 0.3 seconds

# Fixed startup and fail sounds
STARTUP_SOUND = "ST-MARIO.MP3"
FAIL_SOUND = "NO-MARIO.MP3"

# Mystery game volume
GAME_VOLUME = 5  # Max 30

MYSTERY_SOUNDS = {
    # 1-character patterns (2 sounds)
    "L": "TM-SOOTY.MP3",
    "R": "TM-SHARK.MP3",
    # 2-character patterns (4 sounds)
    "LL": "TM-PEPPA.MP3",
    "RR": "TM-SESAM.MP3",
    "LR": "TM-FIREM.MP3",
    "RL": "TM-BLUEY.MP3",
    # 3-character patterns (8 sounds)
    "LLL": "TM-WHEEL.MP3",
    "LLR": "TM-MCDON.MP3",
    "LRL": "TM-MARIO.MP3",
    "LRR": "TM-THOM.MP3",
    "RLL": "TM-PAWP.MP3",
    "RLR": "TM-DRWHO.MP3",
    "RRL": "TM-ROLR.MP3",
    "RRR": "TM-SPID.MP3",
    # 4-character patterns (16 sounds)
    "LLLL": "TM-PRLD.MP3",
    "LLLR": "TM-HIGN.MP3",
    "LLRL": "TM-XFIL.MP3",
    "LLRR": "TM-TBIRD.MP3",
    "LRLL": "TM-QUAN.MP3",
    "LRLR": "TM-ALLO.MP3",
    "LRRL": "TM-STAR.MP3",
    "LRRR": "TM-KNIG.MP3",
    "RLLL": "TM-STARW.MP3",
    "RLLR": "TM-TOPG.MP3",
    "RLRL": "TM-CHRS.MP3",
    "RLRR": "TM-POSTP.MP3",
    "RRLL": "TM-HAWAI.MP3",
    "RRLR": "TM-BLUEY.MP3",
    "RRRL": "TM-NEV.MP3",
    "RRRR": "TM-NEIGH.MP3",
}

# Maximum valid sequence length
MAX_SEQUENCE_LENGTH = max(len(seq) for seq in MYSTERY_SOUNDS.keys())


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

        self.player.play_specific_file(
            FOLDER_PREFIX + STARTUP_SOUND
        )  # Play startup sound
        self.player.set_volume(GAME_VOLUME)
        self.sequence = []
        self.in_game_mode = True
        sleep(DEBOUNCE_DELAY)

    def exit_game_mode(self):
        """
        Exit game mode when both buttons are pressed again.
        """
        self.log("INFO", "Exiting game mode")
        self.in_game_mode = False

    def exit_game_with_fail(self, reason, sequence_str=""):
        """
        Exit the game mode and play the fail sound with a log message.

        :param reason: The reason for exiting the game mode.
        :param sequence_str: The sequence that caused the failure (optional).
        """
        self.log("INFO", f"Exiting game mode due to: {reason}")
        if sequence_str:
            self.log("INFO", f"Sequence that failed: {sequence_str}")
        self.player.play_specific_file(
            FOLDER_PREFIX + FAIL_SOUND
        )  # Play fail sound
        self.exit_game_mode()

    def handle_game_mode(self):
        """
        Handle button presses in game mode.
        """
        if (
            not self.button_left.value() and not self.button_right.value()
        ):  # Both buttons pressed
            self.log("INFO", "Both buttons pressed in game mode")
            self.check_sequence()
            sleep(DEBOUNCE_DELAY)
        elif not self.button_left.value():
            self.log("INFO", "Left button pressed in game mode")
            self.sequence.append("L")
            self.player.play_specific_file(
                FOLDER_PREFIX + "BEEP1.MP3"
            )  # Play beep
            sleep(DEBOUNCE_DELAY)
        elif not self.button_right.value():
            self.log("INFO", "Right button pressed in game mode")
            self.sequence.append("R")
            self.player.play_specific_file(
                FOLDER_PREFIX + "BEEP2.MP3"
            )  # Play boop
            sleep(DEBOUNCE_DELAY)

        # Check if the sequence exceeds the maximum valid length
        if len(self.sequence) > MAX_SEQUENCE_LENGTH:
            self.exit_game_with_fail(
                "Sequence exceeded maximum length", "".join(self.sequence)
            )

    def check_sequence(self):
        """
        Check the collected sequence against the MYSTERY_SOUNDS dictionary.
        """
        sequence_str = "".join(self.sequence)
        self.log("INFO", f"Checking sequence: {sequence_str}")
        if sequence_str in MYSTERY_SOUNDS:
            matched_file = FOLDER_PREFIX + MYSTERY_SOUNDS[sequence_str]
            self.log(
                "INFO",
                f"Sequence matched: {sequence_str}, playing {matched_file}",
            )
            self.player.play_specific_file(matched_file)  # Play success sound
            self.exit_game_mode()
        else:
            self.exit_game_with_fail("Sequence not matched", sequence_str)
