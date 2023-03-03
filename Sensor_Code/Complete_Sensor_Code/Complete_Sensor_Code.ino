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
long timer = millis();

long prevTimeSinceStart = millis();

//Initializing PMW3389's from the library 
PMW3389 sensor1; //uses SS at pin 53 
float x1=0;
float y1=0;  

PMW3389 sensor2; //uses SS at Pin 40 
float x2=0; 
float y2=0; 

float force = 0;

float L_pitch = 0;
float L_yaw = 0;

float R_pitch = 0;
float R_yaw = 0;


float L_PMW_X = 0;
float L_PMW_Y = 0;

float R_PMW_X = 0;
float R_PMW_Y = 0;

float L_yawVel = 0;
float L_yawAcc = 0;
float L_pitchVel = 0;
float L_pitchAcc = 0;
float prev_L_yaw = 0;
float prev_L_yawVel = 0;
float prev_L_yawAcc = 0;
float prev_L_pitch = 0;
float prev_L_pitchVel = 0;
float prev_L_pitchAcc = 0;

float R_yawVel = 0;
float R_yawAcc = 0;
float R_pitchVel = 0;
float R_pitchAcc = 0;
float prev_R_yaw = 0;
float prev_R_yawVel = 0;
float prev_R_yawAcc = 0;
float prev_R_pitch = 0;
float prev_R_pitchVel = 0;
float prev_R_pitchAcc = 0;


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
  unsigned long currentMillis = millis();
  mpu6050_1.update();
  mpu6050_2.update();
  if (currentMillis - timer > 100) {
  
    unsigned long timeSinceStart = millis();
    //MPU gets data from updates
    float L_yaw = mpu6050_1.getAngleY();
    float L_yawVel = 0;
    float L_yawAcc = 0;
    float L_pitch = mpu6050_1.getAngleX();
    float L_pitchVel = 0;
    float L_pitchAcc = 0;

    float R_yaw = mpu6050_2.getAngleY();
    float R_yawVel = 0;
    float R_yawAcc = 0;
    float R_pitch = mpu6050_2.getAngleX();
    float R_pitchVel = 0;
    float R_pitchAcc = 0;

  /* mpu6050_1.update();
    L_pitch = mpu6050_1.getAngleX();
    L_yaw = mpu6050_1.getAngleY();
    L_accX = mpu6050_1.getAccAngleX();
    L_accY = mpu6050_1.getAccAngleY();*/


    //Left MPU velocity and acceleration
    if (prev_L_yaw != 0) {
        L_yawVel = (L_yaw - prev_L_yaw) * 1000.00 / (timeSinceStart - prevTimeSinceStart); // deg/s
      }
      if (prev_L_pitch != 0) {
        L_pitchVel = (L_pitch - prev_L_pitch) * 1000.00 / (timeSinceStart - prevTimeSinceStart); // deg/s
      }

      // Accelerations
    if (prev_L_yawVel != 0) {
      L_yawAcc = (L_yawVel - prev_L_yawVel) * 1000.00 / (timeSinceStart - prevTimeSinceStart); // deg/s^2
    }
    if (prev_L_pitchVel != 0) {
      L_pitchAcc = (L_pitchVel - prev_L_pitchVel) * 1000.00 / (timeSinceStart - prevTimeSinceStart); // deg/s^2
    }

    //Right MPU velocity and acceleration
    if (prev_R_yaw != 0) {
        R_yawVel = (R_yaw - prev_R_yaw) * 1000.00 / (timeSinceStart - prevTimeSinceStart); // deg/s
      }
      if (prev_R_pitch != 0) {
        R_pitchVel = (R_pitch - prev_R_pitch) * 1000.00 / (timeSinceStart - prevTimeSinceStart); // deg/s
      }

      // Accelerations
    if (prev_R_yawVel != 0) {
      R_yawAcc = (R_yawVel - prev_R_yawVel) * 1000.00 / (timeSinceStart - prevTimeSinceStart); // deg/s^2
    }
    if (prev_R_pitchVel != 0) {
      R_pitchAcc = (R_pitchVel - prev_R_pitchVel) * 1000.00 / (timeSinceStart - prevTimeSinceStart); // deg/s^2
    }

    /*mpu6050_2.update();
    R_pitch = mpu6050_2.getAngleX();
    R_yaw = mpu6050_2.getAngleY();
    R_accX = mpu6050_2.getAccX();
    R_accY = mpu6050_2.getAccY();*/

  //Get data from PMW3389 sensors via readburst
    PMW3389_DATA data1 = sensor1.readBurst();
    PMW3389_DATA data2 = sensor2.readBurst(); 

      if (data1.isMotion) {
        L_PMW_X=((data1.dx)/1290) + L_PMW_X; // converts to 1mm since 16,000 CPI 16000=32767 in two's compliment so 32767=16,000=inch=25.4mm therefore 1290=1mmm. 
        L_PMW_Y=((data1.dy)/1290) + L_PMW_Y;  
      }
      if (data2.isMotion) {
        R_PMW_X=((data2.dx)/1290) +R_PMW_X; // converts to 1mm since 16,000 CPI 16000=32767 in two's compliment so 32767=16,000=inch=25.4mm therefore 1290=1mmm. 
        R_PMW_Y=((data2.dy)/1290) +R_PMW_Y;  
      }

      //Force sensor read at Pin A0 
      force = (analogRead(A0)-136) * 0.011; //136 offset to try to "zero" the value
  
      //Serial.println(String(R_pitch) + " " + String(R_pitchAcc) + "   " + String(R_yawAcc));

      Serial.print(String(force) + "|" + String(L_pitchAcc) + "|" + String(L_yawAcc) + "|" + String(R_pitchAcc) + "|" + String(R_yawAcc) + "|" + String(L_PMW_X) + "|"
        + String(L_PMW_Y) + "|" + String(R_PMW_X) + "|" + String(R_PMW_Y) + '\n');
    
      prevTimeSinceStart = timeSinceStart;
      prev_L_yaw = L_yaw;
      prev_L_yawVel = L_yawVel;
      prev_L_yawAcc = L_yawAcc;
      prev_L_pitch = L_pitch;
      prev_L_pitchVel = L_pitchVel;
      prev_L_pitchAcc = L_pitchAcc;

      prev_R_yaw = R_yaw;
      prev_R_yawVel = R_yawVel;
      prev_R_yawAcc = R_yawAcc;
      prev_R_pitch = R_pitch;
      prev_R_pitchVel = R_pitchVel;
      prev_R_pitchAcc = R_pitchAcc;

      //Serial.flush();
    //delay(100); 
  }

}
