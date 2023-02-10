#include <MPU6050_2.h>




#include <MPU6050_1.h>


#include <Wire.h>

MPU6050 mpu6050_1(Wire);
MPU60502 mpu6050_2(Wire); //Addressed at 0x69 and 5V on sensor is connected to AD0 
void setup() {
  Serial.begin(9600);
  Wire.begin();
  mpu6050_1.begin();
  mpu6050_1.calcGyroOffsets(true);
  mpu6050_2.begin(); 
  mpu6050_2.calcGyroOffsets(true); 
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



  Serial.flush();
  
}
