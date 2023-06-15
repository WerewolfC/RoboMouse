"""Presenter class """
from typing import Protocol
from multiprocessing import Process, Pipe
from robomouse.worker import main
from robomouse.utilities import WorkerData


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
        self.mouse_active = None
        self.sent_data = WorkerData()
        self.rcv_conn, self.send_conn = Pipe()

    def copy_worker_data(self, settings):
        """Copy settings data needed for worker"""
        work_data = WorkerData(self.mouse_active,
                               settings.timing_minutes,
                               settings.movement_type)
        print(f'work data to be sent to worker\n\t{work_data}')
        return work_data

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
        self.sent_data = self.copy_worker_data(read_settings)
        print(f'Send data {self.sent_data}')
        self.send_conn.send(self.sent_data)

    def transfer_mouse_state(self, *args):
        """copy mouse active from gui to self and sent data"""
        self.mouse_active = args[0]
        self.sent_data.active_state = args[0]
        print(f'Send data {self.sent_data}')
        self.send_conn.send(self.sent_data)
        #TODO: delete
        print(f'toggle {self.sent_data.active_state}')

    def run(self):
        """Run method of Presenter"""
        self.view.create_gui(self)
        # disable x close main window button
        self.view.protocol("WM_DELETE_WINDOW", disable_event)

        # set the pipe between App and Controller

        self.worker_process = Process(target=main, args=(self.rcv_conn, ))
        self.worker_process.start()

        self.view.mainloop()
