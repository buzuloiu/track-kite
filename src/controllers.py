# from xbox360controller import Xbox360Controller
import numpy as np
import keyboard
from src.track import Camera
from boost_xbox_controller import XBoxControllerManager


class RoboController(object):
    def __init__(self):
        self.xRange = [-600, -475, -425, -325, -225, -125, -25, 0, 25, 125, 225, 325, 425, 475, 600]
        self.xTable = [-1, -0.75, -0.60, -0.45, -0.40, -0.25, -0.05, 0, 0.05, 0.25, 0.40, 0.45, 0.60, 0.75, 1]
        self.yRange = [0, 200, 400, 600, 650, 750, 800, 900, 1000, 1050, 1150, 1200, 1400, 1600, 1800]
        self.yTable = [-1, -0.75, -0.60, -0.45, -0.05, -0.05, -0.05, 0, 0.05, 0.05, 0.05, 0.45, 0.60, 0.75, 1]
        self.current_delta = 0.0
        self.previous_delta = 0.0
        self.maximumDeflectMeters = 7.85e-1
        self.camera = Camera('boardKite')
        self.camera.activate()

    def compute_delta(self):
        frame = self.camera.position
        try:
            xDeflec = np.interp(frame[0], self.xRange, self.xTable)
            xDeflec = np.around(xDeflec, decimals=1)
            #yDeflec = np.interp(frame[1], self.yRange, self.yTable)
            #yDeflec = np.around(yDeflec, decimals=2)
            #yDeflecWeight = np.multiply(yDeflec, 0.1)

            #sumDeflec = np.add(xDeflec, yDeflec)
            #normDeflec = np.divide(sumDeflec, 2)
            self.current_delta = self.maximumDeflectMeters*xDeflec
            self.previous_delta = self.maximumDeflectMeters*xDeflec
        except Exception:
            self.current_delta = self.previous_delta

        return self.current_delta



class XboxController(object):
    def __init__(self, gain=7e-2):
        self.gain = gain
        self.last_read = 0
        self.current_delta = 0.0
        self.xbox_controller_manager = XBoxControllerManager()
        self.success = self.xbox_controller_manager.initialize()
        self.NO_ACTION = 0
        self.LEFT_THUMBSTICK_HORIZONTAL = 1
        self.LEFT_THUMBSTICK_VERTICAL = 2
        self.RIGHT_THUMBSTICK_HORIZONTAL = 3
        self.RIGHT_THUMBSTICK_VERTICAL = 4
        self.BUTTON_PRESSED = 5
        self.BUTTON_RELEASED = 6


    def compute_delta(self):
        event_id, value = self.xbox_controller_manager.get_next_event()
        if event_id is self.LEFT_THUMBSTICK_HORIZONTAL:
            if abs(value) > 30000:
                self.current_delta -= self.gain*np.sign(value)
                self.last_read = value
            else:
                self.last_read = 0
        else:
            self.current_delta -= self.gain*np.sign(self.last_read)
        return self.current_delta

    def active(self):
        return not keyboard.is_pressed('q')



class WASDController(object):
    def __init__(self, gain=7e-2):
        self.gain = gain
        self.last_read = 0
        self.current_delta = 0.0

    def compute_delta(self):
        delta = 0
        if keyboard.is_pressed('a'):
            delta = 1
        elif keyboard.is_pressed('d'):
            delta = -1
        self.current_delta -= self.gain*delta
        return self.current_delta

    def active(self):
        return not keyboard.is_pressed('q')
