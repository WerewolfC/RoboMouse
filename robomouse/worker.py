"""Worker module that implements the mouse movement according to the settings"""
import time
from robomouse.mouseDriver import MouseDriver
from robomouse.utilities import Movement, MouseState, WorkerData

HOURS_TO_MIN_RATIO = 60

class Worker:
    """Implements mouse movement according to settings """
    def __init__(self, active_state, timing, movement, target_pos):
        self.timing = timing
        self.movement = movement
        self.active_state = active_state # info from Togle me button
        self.mouse_driver = MouseDriver()
        self.last_exec_minute = time.localtime(time.time()).tm_min

    def get_no_moves(self):
        """Return number of mouse moves executed"""
        return self.mouse_driver.no_of_moves

    def control_mouse(self, move_method, *args):
        """move the mouse according to the specified method
        to the specified position
        """
        self.mouse_driver.save_coordinates()
        # move to x, y
        new_list = args[0]
        new_list.append( self.mouse_driver.actual_coord_x)
        new_list.append( self.mouse_driver.actual_coord_y)
        move_method(new_list)
        # move to original coordinates
        self.mouse_driver.move_to_original_position()


def main(connection):
    """Main function which is executed as a new process """
    # fetch worker data
    recv_data = WorkerData()
    if connection.poll():
        recv_data = connection.recv()

    worker = Worker(recv_data.active_state,
                    recv_data.loop_period,
                    recv_data.movement_type,
                    recv_data.target_pos)

    while True:
        # create a counter to use for mouse move
        read_minutes = time.localtime(time.time()).tm_min
        if  worker.last_exec_minute > read_minutes:
            read_minutes += HOURS_TO_MIN_RATIO

        #TODO: delete check mouse state and do something
        print("Inside controller")
        print(f'Received data {recv_data}\n of type{type(recv_data)}')
        print(worker.last_exec_minute)

        if connection.poll():
            recv_data = connection.recv()
            print(f'Received data {recv_data}\n of type{type(recv_data)}')

        # check mouse state
        if recv_data.active_state == MouseState.ACTIVE\
            and (read_minutes - worker.last_exec_minute) >= recv_data.loop_period:
            # mouse move
            if recv_data.movement_type == Movement.MOVE_AND_CLICK:
                coord_list = [recv_data.target_pos[0], recv_data.target_pos[1]]
                worker.control_mouse(worker.mouse_driver.to_absolute_position_and_click,
                                     coord_list)
            elif recv_data.movement_type == Movement.JITTER:
                coord_list = [10, 10]
                worker.control_mouse(worker.mouse_driver.to_relative_position,
                                     coord_list)
            worker.last_exec_minute = time.localtime(time.time()).tm_min

        #print(worker.last_exec_minute)
        time.sleep(1)


        # send back number of clicks

        # time.sleep(recv_data.loop_period)
        # time.sleep(1)
