"""Model class """
import pickle
from robomouse.utilities import SettingsElement

SETTINGS_FILE = "settings.bin"


class Model:
    """Model class which implements the settings object, reading and writing of the
    settings using pickle format
    """

    def __init__(self):
        """Load settings data from file if file found,
        else use default values implemented in dataclass
        """

    def get_settings_obj(self):
        """Retuns a settings obj based on the values read from file
        and a use custom flag
        """
        read_settings, read_ok = self.read_pickle_file()

        if read_ok and isinstance(read_settings, SettingsElement):
            returned_settings = read_settings
            use_custom = True
            print('Import OK !')
        else:
            print('Import NOK !')
            use_custom = False
            returned_settings = SettingsElement()
            print(f'Model: data read from dataclass:\n{returned_settings}')
        return returned_settings, use_custom

    def read_pickle_file(self):
        """Open a pickle file and returns ifo
        :return: a tuple (settings_obj, state of the reading)
        state of reading = True -> use read info
        state of reading = False -> use default info
        """
        try:
            with open(SETTINGS_FILE, 'br') as bin_file:
                imported_settings = (pickle.load(bin_file), True)
        except FileNotFoundError:
            imported_settings = (None, False)
        return imported_settings

    def write_pickle_file(self, settings_obj):
        """Writes the actual settings in a bin file """
        with open(SETTINGS_FILE, 'bw') as bin_file:
            pickle.dump(settings_obj, bin_file)
        print(f'data written to file:\n {settings_obj}')
