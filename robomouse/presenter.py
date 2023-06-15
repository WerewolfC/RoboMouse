"""Presenter class """
from typing import Protocol
from multiprocessing import Process, Pipe
from robomouse.worker import main


def disable_event():
    """Empty function used to disable windows close x button"""
    pass


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
        self.worker_process = None

    def handle_exit_button(self):
        """Actions executed when close button is presed"""
        # stop backgroudn process
        # destroy Gui window
        self.worker_process.terminate()
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
            # set the pipe between App and Controller
        rcv_conn, send_conn = Pipe()
        self.worker_process = Process(target=main, args=(rcv_conn, ))
        self.worker_process.start()

        # disable x close main window button
        self.view.protocol("WM_DELETE_WINDOW", disable_event)
        self.view.mainloop()
