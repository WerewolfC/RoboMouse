import pyautogui


class MouseDriver:
    """Class implements the mouse auto driving functionality """

    def __init__(self):
        self._x = 0
        self._y = 0
        self._no_of_moves = 0

    @property
    def actual_coord_x(self):
        return self._x

    @actual_coord_x.setter
    def actual_coord_x(self, value):
        self._x = value

    @property
    def actual_coord_y(self):
        return self._y

    @actual_coord_y.setter
    def actual_coord_y(self, value):
        self._y = value

    def save_coordinates(self):
        self._x, self._y = pyautogui.position()

    def move_to_original_position(self):
        pyautogui.moveTo(self._x, self._y)
        self._no_of_moves += 1

    @staticmethod
    def to_absolute_position_and_click(*args):
        """Moves the mouse to specified position and right click"""
        print(type(args))
        print(args)
        pyautogui.click(args[0][0], args[0][1])

    @staticmethod
    def to_relative_position(*args):
        """Moves the mouse to relative position"""
        pyautogui.moveTo(args[0] + args[2], args[1] + args[3])

    @property
    def no_of_moves(self):
        return self._no_of_moves
