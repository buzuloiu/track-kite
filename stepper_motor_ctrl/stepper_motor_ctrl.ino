#include "motor.h"

const Motor left_motor = {2, 3};
const Motor right_motor = {4, 5};

void setup_motor(int step_pin, int dir_pin) {
  pinMode(motor.step_pin, OUTPUT);
  pinMode(motor.dir_pin, OUTPUT);
  digitalWrite(motor.step_pin, LOW);
}

void setup() {
  setup_motor(left_motor);
  setup_motor(right_motor);

  Serial.begin(9600);
}

void move_motor(Motor &motor, int num_steps) {
  if (num_steps > 0) {
    digitalWrite(motor.dir_pin, HIGH);
  } else {
    digitalWrite(motor.dir_pin, LOW);
  }

  for (int i = 0; i < num_steps; i++){
    digitalWrite(motor.step_pin, HIGH);
    delay(1);
    digitalWrite(motor.step_pin, LOW);
    delay(1);
  }
}

void loop() {
  Serial.println("yo fam");
  while ( true ) {
    move_motor(left_motor, 100);
    move_motor(left_motor, -100);
    move_motor(right_motor, 100);
    move_motor(right_motor, -100);
  }
}

