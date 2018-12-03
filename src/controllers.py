from xbox360controller import Xbox360Controller
from random import randint
import numpy as np
from src.track import Camera

class RoboController(object):
    def __init__(self):
        self.xRange = [-525, -475, -425, -325, -225, -125, -25, 0, 25, 125, 225, 325, 425, 475, 525]
        self.xTable = [-1, -0.75, -0.60, -0.45, -0.40, -0.25, -0.05, 0, 0.05, 0.25, 0.40, 0.45, 0.60, 0.75, 1]
        self.current_delta = 0.0
        self.maximumDeflectMeters = 0.3
        self.camera = Camera('kite')

    def compute_delta(self):

        frame = self.camera.capture_and_process()
        print(frame.time, frame.center)

        commandedDeflection = np.interp(frame.center[0], self.xRange, self.xTable)
        self.maximumDeflectMeters = 0.3*commandedDeflection
        self.current_delta = self.maximumDeflectMeters

        return self.current_delta

class XboxController(object):
    def __init__(self, gain=200):
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
