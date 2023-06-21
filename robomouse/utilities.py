""" Utilities module containing Enum, Const and functions"""
from enum import Enum
from dataclasses import dataclass
from threading import Timer

DEFAULT_TARGET_POS = (0, 500)

def disable_event():
    """Empty function used to disable windows close x button"""
    pass


class MouseState(Enum):
    INACTIVE = 0
    ACTIVE = 1


class Movement(Enum):
    JITTER = 0
    MOVE_AND_CLICK = 1


class Color(Enum):
    GREEN = "green2"
    BLUE = "deep sky blue"
    GOLD = "gold"
    ORANGE = "dark orange"
    RED = "red2"
    PURPLE = "medium purple"
    SNOW = "snow4"
    SLATE_BLUE = "SlateBlue1"
    ORANGE_RED = "OrangeRed2"
    GREY = "light gray"


class SettingsStrings(Enum):
    """Enumerates the setting elements """
    TIMING = "timing"
    MOVEMENT = "movement"
    COLOR_ENABLE = "color_enable"
    COLOR_DISABLE = "color_disable"

    def __str__(self):
        """Override def method to return the formatted item name """
        return " ".join(self.name.split("_")).capitalize()


@dataclass
class SettingsElement:
    """Constains the setting values"""
    timing_minutes: int = 1
    movement_type: Movement = Movement.MOVE_AND_CLICK
    color_enable: Color = Color.GREEN
    color_disable: Color = Color.GREY
    target_pos_xy: tuple = DEFAULT_TARGET_POS


    def __str__(self) -> str:
        """Override the str """
        return f"Timing\t{self.timing_minutes}\n"\
            f"Movement\t{self.movement_type}\n"\
            f"Active color\t{self.color_enable}\n"\
            f"Inactive color\t{self.color_disable}\n"\
            f"Target pos\t{self.target_pos_xy}\n"


@dataclass
class WorkerData:
    """Contains data sent to worker"""
    active_state: MouseState = MouseState.ACTIVE
    loop_period: int = 1
    movement_type: Movement = Movement.MOVE_AND_CLICK
    target_pos: tuple = DEFAULT_TARGET_POS

    def __str__(self) -> str:
        """Override the str """
        return f"Active state\t{self.active_state}\n"\
            f"Loop_period\t{self.loop_period}\n"\
            f"Movement_type\t{self.movement_type}\n"\
            f"Target pos\t{self.target_pos}\n"


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args,**self.kwargs)
