from xbox360controller import Xbox360Controller
from random import randint

class RoboController(object):
    def __init__(self):
        pass

    def compute_delta(self):
        return randint(-50, 50)

class XboxController(object):
    def __init__(self, gain=2):
        self.gain = gain
        self.controller = Xbox360Controller(0, axis_threshold=0.1)
        self.last_read = 0
        self.current_delta = 0.0

    def compute_delta(self):
        left_trigger = self.controller.trigger_l.value
        right_trigger = self.controller.trigger_r.value

        self.current_delta += self.gain*(left_trigger - right_trigger)

        return self.current_delta

    def active(self):
        return not self.controller.button_a.is_pressed
