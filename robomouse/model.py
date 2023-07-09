"""Model class """
import pickle
import logging
from robomouse.utilities import SettingsElement, config_logger


SETTINGS_FILE = "settings.bin"


class Model:
    """Model class which implements the settings object, reading and writing of the
    settings using pickle format
    """

    def __init__(self):
        """Load settings data from file if file found,
        else use default values implemented in dataclass
        """
        self.app_logger = config_logger(logging.getLogger(__name__))

    def get_settings_obj(self):
        """Retuns a settings obj based on the values read from file
        and a use custom flag
        """
        read_settings, read_ok = self.read_pickle_file()

        if read_ok and isinstance(read_settings, SettingsElement):
            returned_settings = read_settings
            use_custom = True
            self.app_logger.info('Import OK !')
        else:
            self.app_logger.warning('Import NOK !!!  Using default settings')
            use_custom = False
            returned_settings = SettingsElement()
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
        except FileNotFoundError as error_not_found:
            self.app_logger.error('%s', error_not_found)
            imported_settings = (None, False)
        return imported_settings

    def write_pickle_file(self, settings_obj):
        """Writes the actual settings in a bin file """
        with open(SETTINGS_FILE, 'bw') as bin_file:
            pickle.dump(settings_obj, bin_file)
        self.app_logger.info('Data written to file: \n%s', settings_obj)
