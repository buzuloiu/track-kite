from src.controllers import XboxController, RoboController
from src.actuators import connect_actuator
import time

CONTROL_LATENCY=1 #s

if __name__ == '__main__':
    active = True

    human_controller = XboxController()
    robot_controller = RoboController()
    actuator = connect_actuator()

    while active:
        delta = None
        if human_controller.active():
            delta = human_controller.compute_delta()
        else:
            delta = robot_controller.compute_delta()

        time.sleep(max(0, CONTROL_LATENCY - (time.time() - actuator.last_update)))
        actuator.set_delta(delta)
