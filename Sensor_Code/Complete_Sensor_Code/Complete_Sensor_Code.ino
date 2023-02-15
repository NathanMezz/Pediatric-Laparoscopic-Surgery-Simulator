#include <MPU6050_2.h>
#include <MPU6050_1.h>
#include <Wire.h>
#include <PMW3389.h>
#include <SPI.h> 

//Initializing MPU's from libraries 
MPU6050 mpu6050_1(Wire);
MPU60502 mpu6050_2(Wire); //Addressed at 0x69 and 5V on sensor is connected to AD0 

/*
# PIN CONNECTION for PMW3389 with reference to Arduino MEGA 2560 
  * MI = MISO Pin 50 
  * MO = MOSI Pin 51 
  * SS = Slave Select / Chip Select depends on PMW3389 see code below 
  * SC = SPI Clock Pin 52 
  * MT = Motion (active low interrupt line) not necessary in this code 
  * RS = Reset not necessary 
  * GD = Ground 
  * VI = Voltage in up to +5.5V
*/

//Initializing PMW3389's from the library 
PMW3389 sensor1; //uses SS at pin 53 
float x1=0;
float y1=0;  

PMW3389 sensor2; //uses SS at Pin 40 
float x2=0; 
float y2=0; 


void setup() {
  Serial.begin(9600);
//MPU portion 
  Wire.begin();
  mpu6050_1.begin();
  mpu6050_1.calcGyroOffsets(true);
  mpu6050_2.begin(); 
  mpu6050_2.calcGyroOffsets(true); 

   while (!Serial);

  sensor1.begin(53, 16000); // to set CPI (Count per Inch), pass it as the //52 is right ss
  sensor2.begin(40,16000); //40 is left ss

}

void loop() {
  //MPU gets data from updates
  mpu6050_1.update();
  Serial.print("Left Pitch: ");
  Serial.print(mpu6050_1.getAngleX());
  Serial.print("\tLeft Yaw: ");
  Serial.print(mpu6050_1.getAngleY());

  mpu6050_2.update();
  Serial.print("\tRight Pitch: ");
  Serial.print(mpu6050_2.getAngleX());
  Serial.print("\tRight Yaw: ");
  Serial.print(mpu6050_2.getAngleY());
  Serial.println("");

//Get data from PMW3389 sensors via readburst
  PMW3389_DATA data1 = sensor1.readBurst();
  PMW3389_DATA data2 = sensor2.readBurst(); 

    if (data1.isOnSurface && data1.isMotion) {
      x1=((data1.dx)/1290) +x1; // converts to 1mm since 16,000 CPI 16000=32767 in two's compliment so 32767=16,000=inch=25.4mm therefore 1290=1mmm. 
      y1=((data1.dy)/1290) +y1;  
      Serial.print("X1:");    
      Serial.print(x1);
      Serial.print(" mm");
      Serial.print("\t");
      Serial.print("Y1:");
      Serial.print(y1);
      Serial.print(" mm   "); 
      Serial.println();
    }
    if (data2.isOnSurface && data2.isMotion) {
      x2=((data2.dx)/1290) +x2; // converts to 1mm since 16,000 CPI 16000=32767 in two's compliment so 32767=16,000=inch=25.4mm therefore 1290=1mmm. 
      y2=((data2.dy)/1290) +y2;  
      Serial.print("\tX2:");    
      Serial.print(x2);
      Serial.print(" mm");
      Serial.print("\t");
      Serial.print("Y2:");
      Serial.print(y2);
      Serial.print(" mm   "); 
      Serial.println();
    }

    //Force sensor read at Pin A0 
    int sensorValue = analogRead(A0);
    Serial.print("Force: ");
    Serial.println(sensorValue);
  delay(100); 


}
