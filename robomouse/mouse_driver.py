"""Mouse driver functionality using PyAutoGUI"""
import pyautogui


class MouseDriver:
    """Class implements the mouse auto driving functionality """

    def __init__(self):
        self._x = 0
        self._y = 0
        self._no_of_moves = 0

    @property
    def actual_coord_x(self):
        """actual coordinates x getter"""
        return self._x

    @actual_coord_x.setter
    def actual_coord_x(self, value):
        """actual coordinates x setter"""
        self._x = value

    @property
    def actual_coord_y(self):
        """actual coordinates y getter"""
        return self._y

    @actual_coord_y.setter
    def actual_coord_y(self, value):
        """actual coordinates y setter"""
        self._y = value

    def save_coordinates(self):
        """save actual coordinates"""
        self._x, self._y = pyautogui.position()

    def move_to_original_position(self):
        """command the mouse driver"""
        pyautogui.moveTo(self._x, self._y)
        self._no_of_moves += 1

    @staticmethod
    def to_absolute_position_and_click(*args):
        """Moves the mouse to specified position and right click"""
        pyautogui.click(args[0][0], args[0][1])

    @staticmethod
    def to_relative_position(*args):
        """Moves the mouse to relative position"""
        pyautogui.moveRel(args[0][0], args[0][1])

    @staticmethod
    def unified_move_action(move_method, *args):
        """Executes the move_method with the arguments"""
        move_method(args[0][0], args[0][1])

    @property
    def no_of_moves(self):
        """property of no_of_moves"""
        return self._no_of_moves
