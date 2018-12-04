import math
from serial import Serial
import time

DEFAULT_COMM_PORT='/dev/ttyACM0'

STEPS_TO_METERS=math.pi*5e-4
STEPS_PER_SECOND=670.

def connect_actuator():
    comm = raw_input("Enter COMM PORT (default {} OR use 'None' to select DummyActuator)".format(DEFAULT_COMM_PORT))
    if comm == "":
        comm = DEFAULT_COMM_PORT
    elif comm == 'None':
        return DummyActuator()

    return Actuator(comm)

class Actuator(object):
    def __init__(self, comm):
        self.next_update=time.time()
        self.delta_steps=0
        self.serial = Serial(comm, baudrate=115200)

        if not self.serial.isOpen():
            self.serial.open()

    def set_delta(self, delta):
        delta_steps = int(delta / STEPS_TO_METERS)
        if delta_steps == self.delta_steps:
            return

        applied_delta = delta_steps - self.delta_steps
        applied_delta = min(127, applied_delta);
        applied_delta = max(-127, applied_delta);

        self.next_update=time.time() + abs(applied_delta)/STEPS_PER_SECOND
        self.serial.write(bytearray([int(128 + applied_delta)]))
        self.delta_steps = delta_steps
        print applied_delta

    def delta(self):
        return STEPS_TO_METERS*self.delta_steps

class MockSerial(object):
    def write(self, msg):
        print msg

class DummyActuator(Actuator):
    def __init__(self):
        self.last_update=time.time()

        self.left_motor_pos=0.0
        self.right_motor_pos=0.0

        self.serial = MockSerial()
