from src.controllers import WASDController, RoboController
from src.actuators import connect_actuator
import time

CONTROL_LATENCY=3#s

if __name__ == '__main__':
    active = True

    human_controller = WASDController()
    robot_controller = RoboController()
    actuator = connect_actuator()

    while active:
        delta = None
        if human_controller.active():
            delta = human_controller.compute_delta()
        else:
            delta = robot_controller.compute_delta()

        absolute = human_controller.compute_absolute()

        if absolute != 0:
            actuator.send_command(absolute, absolute)

        time.sleep(max(0, CONTROL_LATENCY - (time.time() - actuator.last_update)))
        actuator.set_delta(delta)
