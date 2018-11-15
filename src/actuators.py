import math
from serial import Serial


DEFAULT_COMM_PORT='/dev/ttyUSB0'

def connect_actuator():
    comm = input("Enter COMM PORT (default {})".format(DEFAULT_COMM_PORT))
    if comm == "":
        comm = DEFAULT_COMM_PORT

    return Actuators(comm)

class Actuators(object):
    def __init__(self, com_port):
        self.left_motor_pos=0.0
        self.right_motor_pos=0.0
        self.serial = Serial(comm, baudrate=9600)
        self.serial.open()

    def set_delta(self, delta):
        delta -= self.delta()

        left_motor_pos = self.left_motor_pos + math.abs(delta)*int(delta/2)
        right_motor_pos = self.left_motor_pos + math.abs(delta)*int(delta/2)

        send_command(left_motor_pos, right_motor_pos)

    def send_command(self, left_motor_pos, right_motor_pos):
        self.left_motor_pos = left_motor_pos
        self.right_motor_pos= right_motor_pos

        self.serial.write("@Anthony")

    def delta(self):
        return self.left_motor_pos - self.right_motor_pos
