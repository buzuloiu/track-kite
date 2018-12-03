<<<<<<< HEAD
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

  Serial.begin(115200);
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
  char inRead[9] = {'\0'};
  char tmp[5];
  char textA[5];
  char textB[5];
  memset(tmp, 0, sizeof(tmp));

  while (Serial.available() >= 8) {

    for (byte i=0; i<8; i++){
      inRead[i] = Serial.read();
    }

    strncpy(tmp, inRead, 4);
    snprintf(textA, sizeof(textA), "%-4s", tmp);
    strncpy(tmp, &inRead[4], 4);
    Serial.println(textA);
    snprintf(textB, sizeof(textB), "%-4s", tmp);
    Serial.println(textB);

//    if (inRead[0] != "+") {
//      move1 = -1*move1;
//    }
//    if (inRead[4] != "+") {
//      move2 = -1*move2;
//    }
//
//    Serial.println(move1);
//    Serial.println(move2);
//    delay(1000);
//    move_motor(left_motor, move1);
//    move_motor(right_motor, move2);

  inRead[0] = (char)0;
  tmp[0] = (char)0;
  textA[0] = (char)0;
  textB[0] = (char)0;
  }

//  while ( true ) {
//    move_motor(left_motor, 100);
//    move_motor(left_motor, -100);
//    move_motor(right_motor, -100);
//    move_motor(right_motor, 100);
//
//  }

}
=======
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
>>>>>>> initial
