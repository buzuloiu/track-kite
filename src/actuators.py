import math
from serial import Serial
import time

DEFAULT_COMM_PORT='/dev/ttyACM0'

STEPS_TO_METERS=math.pi*5e-4

def connect_actuator():
    comm = raw_input("Enter COMM PORT (default {} OR use 'None' to select DummyActuator)".format(DEFAULT_COMM_PORT))
    if comm == "":
        comm = DEFAULT_COMM_PORT
    elif comm == 'None':
        return DummyActuator()

    return Actuator(comm)

class Actuator(object):
    def __init__(self, comm):
        self.last_update=time.time()
        self.delta=0.0
        self.serial = Serial(comm, baudrate=115200)

        if not self.serial.isOpen():
            self.serial.open()

    def set_delta(self, delta):
        delta /= STEPS_TO_METERS
        self.last_update=time.time()

        new_delta = delta
        delta -= self.delta
        self.delta = new_delta

        delta = min(127, delta);
        delta = max(-127, delta);

        if int(delta) is not 0:
            print int(128+delta)
            self.serial.write(bytearray([int(128 + delta)]))

class MockSerial(object):
    def write(self, msg):
        print msg

class DummyActuator(Actuator):
    def __init__(self):
        self.last_update=time.time()

        self.left_motor_pos=0.0
        self.right_motor_pos=0.0

        self.serial = MockSerial()
