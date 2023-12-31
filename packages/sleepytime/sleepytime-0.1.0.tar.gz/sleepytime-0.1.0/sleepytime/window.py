"""
This is a GUI to prompt you to hibernate your computer.

It can easily be delayed an hour by pressing the delay button.
If you want to cancel the process after that you can right click the system tray icon
and hit exit
"""

import os
import subprocess
import sys
from datetime import datetime, timedelta
from pprint import pformat
from threading import Event, Thread

import PySimpleGUI as sg
from psgtray import SystemTray

from .__version__ import __version__
from .mouse_watcher import wait_for_no_movement
from .resume_watcher import ResumeWatcher

COUNTDOWN_KEY = "countdown"
DELAY_TEXT = "Delay"
SHOW_TEXT = "Show"
HIDE_TEXT = "Hide"
EXIT_TEXT = "Exit"
RESET_HIBERNATE_TIMER = "Reset Hibernate Timer"
FORCE_PASS_MOVEMENT_TEST = "Force Pass Movement Test"
DUMP_INFO_TEXT = "Dump Debug Info"
HIBERNATE_TEXT = "Hibernate"
NO_HIBERNATE_TEXT = "N/A"
DELAY_TIMEDELTA = timedelta(hours=1)
COUNTDOWN_TIMEDELTA = timedelta(minutes=5)

if os.name != "nt":
    raise NotImplementedError(
        "This program only works on Windows.. feel free to PR hibernate calls for other OS's!"
    )


def hibernate_and_exit() -> None:
    """
    Tells Windows to Hibernate NOW and then exits the program

    Funny enough the exit may happen right after the system resumes.
    """
    subprocess.call("shutdown /h", shell=True)

    sys.exit(0)


class SleepyTimeSysTray:
    """
    A wrapper around SystemTray for SleepyTime
    """

    def __init__(self, sleepy_time_window: "SleepyTimeWindow"):
        """
        Initializes the SleepyTimeSysTray with the given SleepyTimeWindow
        """
        self.sys_tray = SystemTray(
            menu=[
                "",
                [
                    "Exit",
                    "Debug",
                    [
                        SHOW_TEXT,
                        HIDE_TEXT,
                        RESET_HIBERNATE_TIMER,
                        FORCE_PASS_MOVEMENT_TEST,
                        DUMP_INFO_TEXT,
                    ],
                ],
            ],
            tooltip="",
            window=sleepy_time_window.window,
        )

        self.sleepy_time_window = sleepy_time_window

    def update(self) -> None:
        """
        Updates the SleepyTimeSysTray. Called by update in SleepyTimeWindow
        """
        # We have access to the sleepy_time_window's last event and values
        if self.sleepy_time_window.last_event == SystemTray.DEFAULT_KEY:
            if (
                self.sleepy_time_window.last_event_values[self.sys_tray.key]
                == SHOW_TEXT
            ):
                self.sleepy_time_window.show()
            elif (
                self.sleepy_time_window.last_event_values[self.sys_tray.key]
                == HIDE_TEXT
            ):
                self.sleepy_time_window.hide()
            elif (
                self.sleepy_time_window.last_event_values[self.sys_tray.key]
                == EXIT_TEXT
            ):
                sys.exit(0)
            elif (
                self.sleepy_time_window.last_event_values[self.sys_tray.key]
                == RESET_HIBERNATE_TIMER
            ):
                # If we set this to None instead, we wouldn't show and start a new one.
                self.sleepy_time_window.hibernate_timer_start_time = datetime.now()
            elif (
                self.sleepy_time_window.last_event_values[self.sys_tray.key]
                == FORCE_PASS_MOVEMENT_TEST
            ):
                self.sleepy_time_window.give_up_is_moving_event.set()
            elif (
                self.sleepy_time_window.last_event_values[self.sys_tray.key]
                == DUMP_INFO_TEXT
            ):
                sys_tray = vars(self)
                window = vars(self.sleepy_time_window)

                txt = (
                    "SleepyTimeSysTray: \n"
                    + pformat(sys_tray)
                    + "\n\n"
                    + "SleepyTimeWindow: \n"
                    + pformat(window)
                )

                sg.popup(
                    txt,
                    title="Debug Info",
                    non_blocking=True,
                    grab_anywhere=True,
                    keep_on_top=True,
                    line_width=120,
                )

        if self.sleepy_time_window.passed_no_movement_test:
            if self.sleepy_time_window.hibernate_timer_start_time is not None:
                self.sys_tray.set_tooltip(
                    f"Sleeping until: {self.sleepy_time_window.hibernate_timer_start_time}"
                )
            else:
                self.sys_tray.set_tooltip(f"SleepTime {__version__} is running...")
        else:
            self.sys_tray.set_tooltip("Waiting for no mouse movement...")


class SleepyTimeWindow:
    """
    A wrapper around PySimpleGUI's Window for SleepyTime
    """

    def __init__(self):
        """
        Initializes the SleepyTimeWindow
        """
        self.window = sg.Window(
            "SleepyTime?",
            [
                [
                    sg.Text("Hibernating in: "),
                    sg.Text(NO_HIBERNATE_TEXT, key=COUNTDOWN_KEY),
                ],
                [
                    sg.Button(DELAY_TEXT, bind_return_key=True, expand_x=True),
                    sg.Button(HIBERNATE_TEXT, expand_x=True),
                ],
            ],
            grab_anywhere=True,
            alpha_channel=0.0,
            no_titlebar=True,
            keep_on_top=True,
            resizable=False,
            disable_close=True,
            disable_minimize=True,
            font=("Arial", 80),
            location=(30, 30),
            finalize=True,
        )
        self.hide()

        # The hibernate timer start time is when we should start the user-facing timer
        self.hibernate_timer_start_time: None | datetime = None

        # The user facing auto-hibernate timer
        self.hibernate_time: None | datetime = None

        # event info from pysimplegui
        self.last_event = ""
        self.last_event_values = dict()

        self.sleepy_time_sys_tray = SleepyTimeSysTray(self)

        # used to tell if we did a hibernation/system resume already
        self.resume_watcher = ResumeWatcher()

        # Someone can set give_up_is_moving_event to act like we passed the mouse move test (and therefore act like the mouse didn't move)
        self.give_up_is_moving_event = Event()
        self._is_moving_thread = Thread(
            target=wait_for_no_movement,
            kwargs=dict(give_up_event=self.give_up_is_moving_event),
            daemon=True,
        )
        self._is_moving_thread.start()

        # Marker to say that we waited for no movement. Set after _is_moving_thread exits.
        self.passed_no_movement_test = False

    def hide(self) -> None:
        """
        Hides the window
        """
        self.window.alpha_channel = 0
        self.window.hide()

    def show(self) -> None:
        """
        Shows the window
        """
        self.window.alpha_channel = 0.8
        self.window.un_hide()

    def start_hibernation_timer(self) -> None:
        """
        Starts the hibernation timer. Also resets the hibernate timer start time so they don't overlap.
        """
        self.hibernate_time = datetime.now() + COUNTDOWN_TIMEDELTA
        self.hibernate_timer_start_time = None

    def run(self) -> None:
        """
        Runs the SleepyTimeWindow. This is the main loop.
        """
        try:
            while True:
                self.update()
                self.sleepy_time_sys_tray.update()
        finally:
            self.window.close()
            self.sleepy_time_sys_tray.sys_tray.close()

    def update(self) -> None:
        """
        Update the sleepytime window. Called over and over by run().

        Will call all functions on this object that end with _if_needed().
        """
        self.last_event, self.last_event_values = self.window.read(timeout=200)

        for name in dir(self):
            if name.endswith("_if_needed"):
                func = getattr(self, name)
                func()

    def _update_countdown_if_needed(self) -> None:
        """
        Based off the hibernate_time, updates the countdown text.
        """
        if self.hibernate_time is None:
            self.window[COUNTDOWN_KEY].update(NO_HIBERNATE_TEXT)
        else:
            span = int(round((self.hibernate_time - datetime.now()).total_seconds()))
            txt = str(max(0, span)) + "s"
            self.window[COUNTDOWN_KEY].update(txt)

    def _hibernate_now_if_needed(self) -> None:
        """
        If the hibernate_time has elapsed OR the hibernate button has been pushed, hibernate and exits.
        """
        if (
            self.hibernate_time is not None and datetime.now() > self.hibernate_time
        ) or self.last_event == HIBERNATE_TEXT:
            hibernate_and_exit()

    def _hide_and_delay_if_needed(self) -> None:
        """
        If the delay button has been pushed, hide the window and set the hibernation timer start time.
        """
        if self.last_event == DELAY_TEXT:
            self.hide()
            self.hibernate_time = None

            self.hibernate_timer_start_time = datetime.now() + DELAY_TIMEDELTA

    def _start_hibernate_timer_if_needed(self) -> None:
        """
        If the hibernate timer start time has elapsed, start the hibernation timer and show the ui.
        """
        if (
            self.hibernate_timer_start_time is not None
            and datetime.now() > self.hibernate_timer_start_time
        ):
            self.start_hibernation_timer()
            self.show()

    def _exit_if_system_has_resumed_if_needed(self) -> None:
        """
        Exits the program if we detected a system resume.
        """
        if self.resume_watcher.is_resumed():
            sys.exit(0)

    def _handle_background_waiting_for_no_movement_if_needed(self) -> None:
        """
        If we haven't passed the no movement test yet, and the is moving thread exited,
        then we passed the no movement test. Set the hibernate timer start time.
        """
        if (
            not self._is_moving_thread.is_alive()
            and self.passed_no_movement_test is False
        ):
            self.passed_no_movement_test = True
            self.hibernate_timer_start_time = datetime.now()
