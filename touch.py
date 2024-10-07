#!/usr/bin/python3

import evdev
import logging
import os

# This is oddly swapped. X is actually the long dimension on the physical screen.
MAX_X = 480
MAX_Y = 640

# Defines left/right touch area
X_MARGIN = 100

# How far to seek fwd/back
SEEK_SECS = 30

# Path to omxplayer control pipe (stdin)
OMXPIPE = "/tmp/omxpipe"


# Function to send commands to omxplayer via stdin (using the named pipe)
def SendOMX(msg: str):
    # Check if the named pipe exists, and create it if it doesn't
    if not os.path.exists(OMXPIPE):
        try:
            os.mkfifo(OMXPIPE)
            logging.info(f"Created omxplayer control pipe at '{OMXPIPE}'")
        except OSError as e:
            logging.error(f"Failed to create pipe: {e}")
            return  # Exit the function if the pipe can't be created

    if msg == "pause":
        os.system(f"echo -n p > {OMXPIPE}")
    elif msg == f"seek {SEEK_SECS}":
        os.system(f"echo -n \x1b[C > {OMXPIPE}")  # Right arrow for seek forward
    elif msg == f"seek {-SEEK_SECS}":
        os.system(f"echo -n \x1b[D > {OMXPIPE}")  # Left arrow for seek backward
    else:
        logging.warning(f"Unrecognized command: {msg}")


# Function to process touch input and send the appropriate command to omxplayer
def Act(x: int, y: int, delta_x: int, delta_y: int):
    # Swipe left
    if delta_x < -(MAX_X / 2):
        logging.info("Detected swipe left (previous)")
        # You can implement playlist prev logic if needed for omxplayer
    # Swipe right
    elif delta_x > MAX_X / 2:
        logging.info("Detected swipe right (next)")
        # You can implement playlist next logic if needed for omxplayer
    # Left touch
    elif x < X_MARGIN:
        logging.info(f"Seeking backward {SEEK_SECS} seconds")
        SendOMX(f"seek {-SEEK_SECS}")
    # Right touch
    elif x > MAX_X - X_MARGIN:
        logging.info(f"Seeking forward {SEEK_SECS} seconds")
        SendOMX(f"seek {SEEK_SECS}")
    # Middle touch
    else:
        logging.info("Toggling pause/play")
        SendOMX("pause")


def main():
    logging.getLogger().setLevel(logging.INFO)

    # Device path for the touch input, adjust this if needed
    device = evdev.InputDevice("/dev/input/event0")
    logging.info("Input device: %s", device)

    # Key event comes before location event. Assume first key down is in middle of screen
    x = int(MAX_X / 2)
    y = int(MAX_Y / 2)

    down_x = None
    down_y = None

    # Read input events in a loop
    for event in device.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            if event.code == evdev.ecodes.BTN_TOUCH:
                if event.value == 0x0:  # Touch release
                    delta_x = x - down_x
                    delta_y = y - down_y
                    Act(x, y, delta_x, delta_y)
                if event.value == 0x1:  # Touch down
                    down_x = x
                    down_y = y
        elif event.type == evdev.ecodes.EV_ABS:
            # Screen is rotated, so X & Y are swapped from how the input reports them.
            if event.code == evdev.ecodes.ABS_MT_POSITION_X:
                y = MAX_Y - event.value
            elif event.code == evdev.ecodes.ABS_MT_POSITION_Y:
                x = MAX_X - event.value


if __name__ == "__main__":
    main()
