"""
Home to functionality related to watching the mouse.
"""
from datetime import timedelta
from time import sleep, time

from pyautogui import position


def is_moving(max_wait: timedelta = timedelta(minutes=5)) -> bool:
    """
    Returns whether or not the mouse is moving at least once. Will wait up to max_wait for the mouse to move.
    """

    last_positions = set()
    death_time = time() + max_wait.total_seconds()

    while time() < death_time:
        last_positions.add(position())

        if len(last_positions) > 1:
            return True

        sleep(1)

    return len(last_positions) > 1
