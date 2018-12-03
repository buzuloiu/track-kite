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

        self.left_motor_pos=0.0
        self.right_motor_pos=0.0

        self.serial = Serial(comm, baudrate=115200)

        if not self.serial.isOpen():
            self.serial.open()

    def set_delta(self, delta):
        delta -= self.delta()

        move_left = delta/2
        move_right = -1 * move_left

        self.send_command(move_left, move_right)


    def send_command(self, move_left, move_right):
        self.left_motor_pos += move_left
        self.right_motor_pos += move_right

        move_left /= STEPS_TO_METERS
        move_right /= STEPS_TO_METERS
        move_left=int(move_left)
        move_right=int(move_right)

        if move_left not in range(-999, 1000) or move_right not in range(-999, 1000):
            print 'movement [{}, {}] out of range [-999, 999]'.format(move_left, move_right)
            raise
        #elif move_left == 0 or move_right == 0:
        #    return

        self.last_update=time.time()
        cmd = (
            '{:+d}'.format(int(move_left)).zfill(4) +
            '{:+d}'.format(int(move_right)).zfill(4)
        )
        print cmd
        self.serial.write(cmd)

    def delta(self):
        return self.left_motor_pos - self.right_motor_pos

class MockSerial(object):
    def write(self, msg):
        pass

class DummyActuator(Actuator):
    def __init__(self):
        self.last_update=time.time()

        self.left_motor_pos=0.0
        self.right_motor_pos=0.0

        self.serial = MockSerial()
