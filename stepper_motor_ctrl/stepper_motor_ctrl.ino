#include "motor.h"

const Motor left_motor = {3, 2, 6};
const Motor right_motor = {5, 4, 7};

int serial_data = 0;

void setup_motor(Motor motor) {
  pinMode(motor.step_pin, OUTPUT);
  pinMode(motor.dir_pin, OUTPUT);
  pinMode(motor.disable_pin, OUTPUT);
  digitalWrite(motor.step_pin, LOW);
  digitalWrite(motor.disable_pin, LOW);
}

void setup() {
  pinMode(13, OUTPUT);
  setup_motor(left_motor);
  setup_motor(right_motor);

  Serial.begin(115200);
}

void move_motor(int num_steps) {
  if (num_steps > 0) {
    digitalWrite(left_motor.dir_pin, HIGH);
    digitalWrite(right_motor.dir_pin, HIGH);
  } else {
    digitalWrite(left_motor.dir_pin, LOW);
    digitalWrite(right_motor.dir_pin, LOW);
    num_steps = -1*num_steps;
  }

  while(num_steps > 0) {
    delayMicroseconds(800);
    digitalWrite(left_motor.step_pin, HIGH);
    digitalWrite(right_motor.step_pin, HIGH);
    delayMicroseconds(800);
    digitalWrite(left_motor.step_pin, LOW);
    digitalWrite(right_motor.step_pin, LOW);
    num_steps--;
  }
}

void toggle_motor(Motor motor) {
 if (motor.disabled) {
   motor.disabled = false;
   digitalWrite(motor.disable_pin, HIGH);
 } else {
   motor.disabled = true;
   digitalWrite(motor.disable_pin, LOW);
 }
}

void loop() {
  if (Serial.available() > 0) {
    serial_data = Serial.read() - 128;
    if (serial_data != 0) {
      move_motor(serial_data);
    }
  }
}
