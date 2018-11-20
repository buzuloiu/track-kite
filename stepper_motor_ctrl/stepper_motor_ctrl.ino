#include "motor.h"

const Motor left_motor = {3, 2};
const Motor right_motor = {5, 4};

void setup_motor(Motor motor) {
  pinMode(motor.step_pin, OUTPUT);
  pinMode(motor.dir_pin, OUTPUT);
  digitalWrite(motor.step_pin, LOW);
}

void setup() {
  setup_motor(left_motor);
  setup_motor(right_motor);

  Serial.begin(9600);
}

void move_motor(Motor motor, int num_steps) {
  if (num_steps > 0) {
    digitalWrite(motor.dir_pin, HIGH);
  } else {
    digitalWrite(motor.dir_pin, LOW);
    num_steps = -1*num_steps;
  }

  for (int i = 0; i < num_steps; i++){
    delay(1);
    digitalWrite(motor.step_pin, HIGH);
    delay(1);
    digitalWrite(motor.step_pin, LOW);
  }
}

void loop() {
  while (Serial.available() < 1) {
    String read_str = Serial.readString();
    String sign1 = read_str.substring(0,1);
    String sign2 = read_str.substring(4,5);
    String str1 = read_str.substring(1, 4);
    String str2 = read_str.substring(5, 8);

//    int sign1 = sign1s.toInt();
//    int sign2 = sign2s.toInt();
    int move1 = str1.toInt();
    int move2 = str2.toInt();
    if (sign1 != "+"){
      move1 = -1*move1;
    }
    if (sign2 == "+"){
      move2 = -1*move2;
    }

    move_motor(left_motor, move1);
    move_motor(right_motor, move2);
  }

//  while ( true ) {
//    move_motor(left_motor, 100);
//    move_motor(left_motor, -100);
//    move_motor(right_motor, -100);
//    move_motor(right_motor, 100);
//
//  }
}
