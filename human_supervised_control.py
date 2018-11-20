from src.controllers import XboxController, RoboController
from src.actuators import connect_actuator
import time

CONTROL_LATENCY=0.5

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

        time.sleep(max(0, time.time()-actuator.last_update))
        actuator.set_delta(delta)
