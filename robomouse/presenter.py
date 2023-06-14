"""Presenter class """
from typing import Protocol


class View(Protocol):
    def create_gui(self):
        ...

    def mainloop(self):
        ...

    def destroy(self):
        ...

    def update_settings(self, settings_obj):
        ...


class Presenter:
    """Presenter class """
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def handle_exit_button(self):
        """Actions executed when close button is presed"""
        # stop backgroudn process
        # destroy Gui window
        self.view.destroy()

    def handle_get_saved_settings(self):
        """Gets saved settings from the model"""
        return self.model.get_settings_obj()

    def handle_save_settings_data(self, *args):
        """Actions executed when save settings button is pressed"""
        active_settings = args[0]
        # write settings to file
        self.model.write_pickle_file(active_settings)

        # read settings from model
        read_settings, _ = self.model.get_settings_obj()

        # update settings element in view
        self.view.update_settings(read_settings)

        # Presenter update sent to bkg process settings values


    def run(self):
        """Run method of Presenter"""
        self.view.create_gui(self)
        self.view.mainloop()
