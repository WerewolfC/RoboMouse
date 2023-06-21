"""Presenter class """
from typing import Protocol
from multiprocessing import Process, Pipe
from robomouse.worker import main
from robomouse.utilities import WorkerData, RepeatTimer, disable_event


def read_from_thread(presenter):
    """Executed by Timer thread
    implements the Pipe rcv method
    """
    if presenter.parent_connection.poll():
        recv_data = presenter.parent_connection.recv()
        print(f'Thread > Data reveived {recv_data}', flush=True)
        presenter.view.update_executions(str(recv_data))


class View(Protocol):
    def create_gui(self):
        ...

    def mainloop(self):
        ...

    def destroy(self):
        ...

    def update_settings(self, settings_obj):
        ...

    def update_executions(self, value):
        ...


class Presenter:
    """Presenter class """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.worker_process = None
        self.mouse_active = None
        self.sent_data = WorkerData()
        self.child_connection, self.parent_connection = Pipe(duplex=True)
        self.timer_thread = None

    def copy_worker_data(self, settings):
        """Copy settings data needed for worker"""
        work_data = WorkerData(self.view.mouse_state,
                               settings.timing_minutes,
                               settings.movement_type,
                               settings.target_pos_xy)
        return work_data

    def handle_exit_button(self):
        """Actions executed when close button is presed"""
        # stop backgroudn process
        self.worker_process.terminate()
        # destroy Gui window
        self.view.destroy()

        # kill timer thread
        self.timer_thread.cancel()

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
        print(f'Presenter > Send data \n{self.sent_data}')
        self.parent_connection.send(self.sent_data)

    def transfer_mouse_state(self, *args):
        """copy mouse active from gui to self and sent data"""
        self.mouse_active = args[0]
        self.sent_data.active_state = args[0]
        #TODO
        print(f'Presenter > Send data \n{self.sent_data}')
        self.parent_connection.send(self.sent_data)

    def run(self):
        """Run method of Presenter"""
        self.view.create_gui(self)
        # disable x close main window button
        self.view.protocol("WM_DELETE_WINDOW", disable_event)
        #initialize sent data
        self.sent_data = self.copy_worker_data(self.model.get_settings_obj()[0])
        # set the pipe between App and Controller
        self.worker_process = Process(target=main,
                                      args=(self.child_connection,
                                            self.sent_data))
        self.worker_process.start()

        # create timer thread
        self.timer_thread = RepeatTimer(10, read_from_thread, [self])
        self.timer_thread.start() #recalling run
        print('Presenter > starting thread timer', flush=True)

        self.view.mainloop()
