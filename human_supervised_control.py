from src.controllers import XboxController, RoboController
from src.actuators import connect_actuator

if __name__ == '__main__':
    # actuator = connect_actuator()
    human_controller = XboxController()
    robot_controller = RoboController()

    active_controller = human_controller

    def human_take_control(button):
        import pdb; pdb.set_trace()
        active_controller = human_controller

    def human_release_control(button):
        import pdb; pdb.set_trace()
        active_controller = robot_controller

    human_controller.controller.button_a.when_pressed = human_release_control
    human_controller.controller.button_a.when_released = human_take_control

    while True:
        print active_controller.compute_delta()
