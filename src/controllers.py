from time import time
from xbox360controller import Xbox360Controller
MAX_STEPS_SECOND = 1./200.

class RoboController(object):
    def __init__(self):
        pass

    def compute_delta(self):
        return "ROBOT"

class XboxController(object):
    def __init__(self):
        self.controller = Xbox360Controller(0, axis_threshold=0.1)
        self.last_read = 0
        self.current_delta = 0.0

    def compute_delta(self):
        if (time() - self.last_read) < MAX_STEPS_SECOND:
            return self.current_delta

        left_trigger = self.controller.trigger_l.value
        right_trigger = self.controller.trigger_r.value

        self.current_delta += (left_trigger - right_trigger)
        self.last_read = time()

        return self.current_delta
