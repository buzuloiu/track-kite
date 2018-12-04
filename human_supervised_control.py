from src.controllers import WASDController, RoboController
from src.actuators import connect_actuator
import time
import cv2

if __name__ == '__main__':
    active = True

    human_controller = WASDController()
    robot_controller = RoboController()
    actuator = connect_actuator()

    print 'Starting'
    while active:
        delta = None
        if human_controller.active():
            delta = human_controller.compute_delta()
        else:
            delta = robot_controller.compute_delta()

        time.sleep(max(0, actuator.next_update - time.time()))
        actuator.set_delta(delta)
