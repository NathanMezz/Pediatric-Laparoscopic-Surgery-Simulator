#include <MPU6050_2.h>




#include <MPU6050_1.h>


#include <PMW3389.h>
#include <SPI.h>

#include <Wire.h>

#define MOT 2 // motion interrupt pin, connect this pin to MT on the module.
#define SS 53 //was 10 Slave Select pin. Connect this to SS on the module.

PMW3389 sensor;
volatile bool motion = false;
int x=0;
int y=0;  
int count=0;

MPU6050 mpu6050_1(Wire);
MPU60502 mpu6050_2(Wire); //Addressed at 0x69 and 5V on sensor is connected to AD0 
void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu6050_1.begin();
  mpu6050_1.calcGyroOffsets(true);
  mpu6050_2.begin(); 
  mpu6050_2.calcGyroOffsets(true); 

  sensor.begin(53, 16000); // to set CPI (Count per Inch), pass it as the
  // second parameter
  pinMode(MOT, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(MOT), motionDetected, FALLING);

  if (digitalRead(MOT) == LOW)
    motion = true;
}

void loop() {
 
  mpu6050_1.update();
  
  Serial.print("Left Pitch: ");
  Serial.print(mpu6050_1.getAngleX());
  
  Serial.print("\tLeft Yaw: ");
  Serial.print(mpu6050_1.getAngleY());
 // Serial.println(""); 
 // Serial.print("\tangleZ1 : ");
 // Serial.println(mpu6050_1.getAngleZ());
  
  //Serial.print("\tPitch Accel:");
  //Serial.print(mpu6050_1.getAccX()*9.8);
  
  //Serial.print("\tYaw Accel:");
  //Serial.print(mpu6050_1.getAccAngleY());
  //Serial.println("                   "); 


  
  mpu6050_2.update();
  Serial.print("\tRight Pitch: ");
  Serial.print(mpu6050_2.getAngleX());
  Serial.print("\tRight Yaw: ");
  Serial.print(mpu6050_2.getAngleY());
  //Serial.print("\tangleZ2 : ");
  //Serial.println(mpu6050_2.getAngleZ());

  int sensorValue = analogRead(A0);

  Serial.print("\t");
  Serial.print(sensorValue);
  Serial.println("");

  if (motion) {
    
    cli(); // disable interrupt during motion data processing.
    PMW3389_DATA data = sensor.readBurst(); // read sensor data.

    x=((data.dx)/1290) +x; // converts to 1mm since 16,000 CPI 16000=32767 in two's compliment so 32767=16,000=inch=25.4mm therefore 1290=1mmm. 
    y=((data.dy)/1290) +y;  
    count=count+1; 
    Serial.print("X:");    
    Serial.print(x);
    Serial.print(" mm");
    Serial.print("\t");
    Serial.print("Y:");
    Serial.print(y);
    Serial.print(" mm   "); 
    Serial.print(count);
    Serial.println();

 

    motion = false;
    sei(); // enable interrupt again.
    delay(100);

    //Serial.flush();
  }

  Serial.flush();
  
}

void motionDetected() // interrupt service routine should be minimized.
{
  motion = true; // flag setting.
}
