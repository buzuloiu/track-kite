from src.controllers import WASDController, RoboController, XboxController
from src.actuators import connect_actuator
import time
import cv2

if __name__ == '__main__':
    active = True

    # human_controller = WASDController()
    human_controller = XboxController()

    robot_controller = RoboController()
    actuator = connect_actuator()

    cv2.startWindowThread()
    cv2.namedWindow("video_feed")
    print 'Starting'

    while active:
        delta = None
        if human_controller.active():
            delta = human_controller.compute_delta()
        else:
            delta = robot_controller.compute_delta()

        time.sleep(max(0, actuator.next_update - time.time()))
        actuator.set_delta(delta)
        cv2.imshow('video_feed', robot_controller.camera.image)
        if cv2.waitKey(1) == 27:
            break
    robot_controller.camera.stream.stop()
    cv2.destroyAllWindows()
    robot_controller.camera.deactivate()
