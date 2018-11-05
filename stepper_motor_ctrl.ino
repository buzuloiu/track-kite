#include <Stepper.h>

const double pi = 3.1415926;
const int stepsPerRevolution = 200;
int stepperSpeed = 60;
const double innerRad = ;
                          
Stepper myStepper1(stepsPerRevolution,2,3,4,5);
Stepper myStepper2(stepsPerRevolution,8,9,10,11);

void setup() {
  myStepper1.setSpeed(stepperSpeed);
  myStepper2.setSpeed(stepperSpeed);

  Serial.begin(9600);
  
}

void loop() {
  if (Serial.avaliable()) {
    double differential = Serial.parseFloat();
    int stepCount = diff2steps( differential/2 );

    myStepper1.step(stepCount);
    myStepper2.step(-stepCount);
  }
  delay(250);
}

int diff2steps(double diff) {
  double lenPerStep = (1.8/180*pi)*innerRad;
  int stepCount = round( diff/lenPerStep );
  return stepCount;
}
