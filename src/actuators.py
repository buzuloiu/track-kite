import math
from serial import Serial
import time

DEFAULT_COMM_PORT='/dev/ttyUSB0'

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

        self.left_motor_pos=0.0
        self.right_motor_pos=0.0

        self.serial = Serial(comm, baudrate=9600)
        self.serial.open()

    def set_delta(self, delta):
        delta -= self.delta()

        move_left = math.ceil(delta/2)
        move_right = -1 * math.floor(delta/2)

        self.send_command(move_left, move_right)


    def send_command(self, move_left, move_right):
        self.left_motor_pos += move_left
        self.right_motor_pos += move_right

        self.last_update=time.time()
        self.serial.write('{:+4d}{:+4d}'.format(int(move_left), int(move_right)))

    def delta(self):
        return self.left_motor_pos - self.right_motor_pos

class MockSerial(object):
    def write(self, msg):
        print msg

class DummyActuator(Actuator):
    def __init__(self):
        self.last_update=time.time()

        self.left_motor_pos=0.0
        self.right_motor_pos=0.0

        self.serial = MockSerial()
