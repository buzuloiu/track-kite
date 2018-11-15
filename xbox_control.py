from src.controllers import XboxController
from src.actuators import connect_actuator

if __name__ == '__main__':
    controller = XboxController()

    while True:
        print controller.compute_delta()
