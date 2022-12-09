#include <Wire.h>
const int MPU2 = 0x69, MPU1=0x68;

//Data Values for Left MPU located at 0x68
long accelX, accelY, accelZ; 
float gForceX, gForceY, gForceZ, gyroX, gyroY, gyroZ,rotX, rotY, rotZ;

//Data Values for Right MPU Located at 0x69
long accelX2, accelY2, accelZ2;
float gForceX2, gForceY2, gForceZ2, gyroX2, gyroY2, gyroZ2, rotX2, rotY2, rotZ2;;


void setup(){
//Setting up I2C Communication for MPU1    
  Serial.begin(19200);
  Wire.begin();
  Wire.beginTransmission(MPU1);
  Wire.write(0x6B);
  Wire.write(0b00000000);
  Wire.endTransmission();  
  Wire.beginTransmission(MPU1);
  Wire.write(0x1B);
  Wire.write(0x00000000);
  Wire.endTransmission(); 
  Wire.beginTransmission(MPU1);
  Wire.write(0x1C);
  Wire.write(0b00000000);
  Wire.endTransmission(); 
  
  //Setting up I2C Communication for MPU2 
  Wire.begin();
  Wire.beginTransmission(MPU2);
  Wire.write(0x6B);
  Wire.write(0b00000000); 
  Wire.endTransmission();  
  Wire.beginTransmission(MPU2); 
  Wire.write(0x1B);
  Wire.write(0x00000000);
  Wire.endTransmission(); 
  Wire.beginTransmission(MPU2);
  Wire.write(0x1C);
  Wire.write(0b00000000);
  Wire.endTransmission(); 
  
  
}

void loop(){
  //Begins I2C Register reading from the MPU6050 Register map 
  Serial.println(""); 
  Serial.print("MPU1:                                MPU2:"); 
 
  Wire.beginTransmission(MPU1); 
  Wire.write(0x3B);
  Wire.endTransmission();
  Wire.requestFrom(MPU1,6);
  while(Wire.available() < 6);
  accelX = Wire.read()<<8|Wire.read(); 
  accelY = Wire.read()<<8|Wire.read(); 
  accelZ = Wire.read()<<8|Wire.read();
  
  Wire.beginTransmission(MPU1);
  Wire.write(0x43);
  Wire.endTransmission();
  Wire.requestFrom(MPU1,6);
  while(Wire.available() < 6);
  gyroX = Wire.read()<<8|Wire.read();
  gyroY = Wire.read()<<8|Wire.read();
  gyroZ = Wire.read()<<8|Wire.read(); 


  gForceX = accelX / 16384.0;
  gForceY = accelY / 16384.0; 
  gForceZ = accelZ / 16384.0;
  rotX = gyroX / 131.0;
  rotY = gyroY / 131.0; 
  rotZ = gyroZ / 131.0;
  Serial.println(""); 
  Serial.print("gyro and rotation\t");
  Serial.print(rotX);
  Serial.print(gyroX);
  Serial.print("\t");
  Serial.print(rotY);
  Serial.print(gyroY);
  Serial.print("\t");
  Serial.print(rotZ);
  Serial.print(gyroZ);
  Serial.println(""); 
  Serial.print("Acc\t");
  Serial.print(gForceX);
  Serial.print("\t");
  Serial.print(gForceY);
  Serial.print("\t");
  Serial.print(gForceZ);  

  //Begins I2C Register Reading from MPU6050 Register map 
  Wire.beginTransmission(MPU2); 
  Wire.write(0x3B);
  Wire.endTransmission();
  Wire.requestFrom(MPU2,6);
  while(Wire.available() < 6);
  accelX2 = Wire.read()<<8|Wire.read(); 
  accelY2 = Wire.read()<<8|Wire.read(); 
  accelZ2 = Wire.read()<<8|Wire.read();
  
  Wire.beginTransmission(MPU2);
  Wire.write(0x43);
  Wire.endTransmission();
  Wire.requestFrom(MPU2,6);
  while(Wire.available() < 6);
  gyroX2 = Wire.read()<<8|Wire.read();
  gyroY2 = Wire.read()<<8|Wire.read();
  gyroZ2 = Wire.read()<<8|Wire.read(); 


  gForceX2 = accelX2 / 16384.0;
  gForceY2 = accelY2 / 16384.0; 
  gForceZ2 = accelZ2 / 16384.0;
  rotX2= gyroX2 / 131.0;
  rotY2 = gyroY2 / 131.0; 
  rotZ2 = gyroZ2 / 131.0;
  Serial.print("    gyro\t");
  Serial.print(rotX);
  Serial.print(gyroX2);
  Serial.print("\t");
  Serial.print(rotY);
  Serial.print(gyroY2);
  Serial.print("\t");
  Serial.print(rotZ);
  Serial.print(gyroZ2);
  Serial.println(""); 
  Serial.print("                                 Acc\t");
  Serial.print(gForceX);
  Serial.print("\t");
  Serial.print(gForceY);
  Serial.print("\t");
  Serial.print(gForceZ);
  
  delay(100);
}


