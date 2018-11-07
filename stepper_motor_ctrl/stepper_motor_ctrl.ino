int x;

const double pi = 3.1415926;
const int stepsPerRevolution = 200;
int stepperSpeed = 60;
const double innerRad = 0.05;

const int dirPin1 = 2; 
const int stepPin1 = 3;
const int dirPin2 = 4; 
const int stepPin2 = 5;

void setup() {
  pinMode(stepPin1,OUTPUT); 
  pinMode(dirPin1,OUTPUT);
  pinMode(stepPin2,OUTPUT); 
  pinMode(dirPin2,OUTPUT);

  Serial.begin(9600);
}

void loop() {
  sweep();
//  if (Serial.avaliable()) {
//    double differential = Serial.parseFloat();
//    int stepCount = diff2steps( differential/2 );
//    
//    if (differential < 0) {
//      digitalWrite(dirPin1,HIGH);
//      digitalWrite(dirPin2,LOW);
//      driveStepper1();
//      driveStepper2();
//    }
//    else {
//      digitalWrite(dirPin1,LOW);
//      digitalWrite(dirPin2,HIGH);
//      driveStepper2();
//      driveStepper1();
//    }    
//  }
//  delay(500);

}

int diff2steps(double diff) {
  double lenPerStep = (1.8/180*pi)*innerRad;
  int stepCount = round( diff/lenPerStep );
  
  return stepCount;
}

void sweep(){
  digitalWrite(stepPin1,HIGH); // Set Dir high
  for(x = 0; x < 200; x++) {
    digitalWrite(stepPin1,HIGH);
    delay(10);
    digitalWrite(stepPin1,LOW);
  }
  delay(1000);
  digitalWrite(stepPin1,LOW); 
  for(x = 0; x < 200; x++) {
    digitalWrite(stepPin1,HIGH);
    delay(10);
    digitalWrite(stepPin1,LOW);
  }
  delay(1000);
  
  digitalWrite(stepPin2,HIGH); // Set Dir high
  for(x = 0; x < 200; x++) {
    digitalWrite(stepPin2,HIGH);
    delay(10);
    digitalWrite(stepPin2,LOW);
  }
  delay(1000);
  digitalWrite(stepPin2,LOW);
  for(x = 0; x < 200; x++) {
    digitalWrite(stepPin2,HIGH);
    delay(10);
    digitalWrite(stepPin2,LOW);
  }
  delay(1000);
}

void driveStepper1(int stepCount) {
  for (x = 0; x < stepCount; x++) {
    digitalWrite(stepPin1, HIGH);
    delay(10);
    digitalWrite(stepPin1, LOW);
  }
}

void driveStepper2(int stepCount) {
  for (x = 0; x < stepCount; x++) {
    digitalWrite(stepPin2, HIGH);
    delay(10);
    digitalWrite(stepPin2, LOW);
  }
}
