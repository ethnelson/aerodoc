#include <DFRobot_SHT3x.h>
#include <DFRobot_EC.h>

DFRobot_SHT3x tempProbe;
DFRobot_EC elect;
boolean newData = false;
const byte numChars = 32;
char receivedChars[numChars];
float payload = -1;

// -------------------------------------------------------------------------- //
//                               PIN MAPPING                                  //
// -------------------------------------------------------------------------- //
// ------------------------------ sensor pins ------------------------------- //

int ec = A0;
int ph = A1;
int wat = A2;
// --------------------------- controller pins ------------------------------ //
int light = 7;
int fan = 6;

// Peristaltic pumps 1-3
int p1 = 8;
int p2 = 9;
int p3 = 10;

// --------------------------- EC & PH Offsets ------------------------------ //
int ec_offset = 1.28;
int ph_offset = .3;

// --------------------- Perisaltic Pump Calibration ------------------------ //
// the amout of time it takes the pump to dispense 5 ml of fluid
int pumpTime = 9000;


void setup() {
  Serial.begin(9600);
  tempProbe.begin();
  elect.begin();
  pinMode(p1, OUTPUT);
  pinMode(p2, OUTPUT);
  pinMode(p3, OUTPUT);
  pinMode(light, OUTPUT);
  pinMode(fan, OUTPUT);
}

void loop() {
  retrieveData();
  if (newData == true)
  {
    Serial.println(receivedChars);
    dataSwitch();
    newData = false;
  }
}
// -------------------------------------------------------------------------- //
//                             READING SERIAL                                 //
// -------------------------------------------------------------------------- //
void retrieveData()
{
  static byte index;
  char endMarker = '\n';
  char rc;

  while (Serial.available() > 0 && newData == false)
  {
    rc = Serial.read();
    if (rc != endMarker)
    {
      receivedChars[index] = rc;
      index++;
      if (index >= numChars)
      {
        index = numChars - 1;
      }
    }
    else
    {
      receivedChars[index] = '\0';
      index = 0;
      newData = true;
    }
  }
}
// -------------------------------------------------------------------------- //
//                          ACTIONS BASED ON SERIAL                           //
// -------------------------------------------------------------------------- //
void dataSwitch()
{
  float payload = -2;

  // ---------------------------- SENSOR READING  --------------------------- //
  // E - EC sensor
  // P - PH sensor
  // T - Temperature Sensor
  // H - Humidity Sensor
  // W - Water level sensor

  if (receivedChars[0] == 'S')
  {
    payload = -15;
    if (receivedChars[1] == 'E')
    {
      //Read EC Sensor
      float temp;
      payload = analogRead(ec);
      payload = payload/1024;
      payload = payload*5000;
      temp = tempProbe.getTemperatureC();
      payload = elect.readEC(payload, temp);
      payload = payload*ec_offset;
    }
    else if (receivedChars[1] == 'P')
    {
      //Read PH Sensor
      payload = analogRead(ph);
      payload = payload*5;
      payload = payload/1024;
      payload = payload*3.5;
      payload += ph_offset;
    }
    else if (receivedChars[1] == 'T')
    {
      //Read Temperature Sensor
      payload = tempProbe.getTemperatureC();
    }
    else if (receivedChars[1] == 'H')
    {
      //Read Humidity Sensor
      payload = tempProbe.getHumidityRH();
    }
    else if (receivedChars[1] == 'W')
    {
      payload = analogRead(wat);
      if (payload != 0){
        payload = 1;
      }
    }
  }
    // ------------------------- CONTROLLER SECTION ------------------------- //
    // L - control the lights (on/off)
    // F - control the fan (on/off)
    // U - Peristaltic pump control
    //    1 - pump #1
    //    2 - pump #2
    //    3 - pump #3
    //
    // When specifying the action for the control (on/off) 'H' and 'L' are used to
    // specify if the voltage is HIGH or LOW
  else if (receivedChars[0] == 'C')
  {
    // LIGHT CONTROL
    if (receivedChars[1] == 'L')
    {
      if (receivedChars[2] == 'H')
      {
        digitalWrite(light, HIGH);
        payload = 0;
      }
      else if (receivedChars[2] == 'L')
      {
        digitalWrite(light, LOW);
        payload = 0;
      }
    }
    // FAN CONTROL
    else if (receivedChars[1] == 'F')
    {
      if (receivedChars[2] == 'H')
      {
        digitalWrite(fan, HIGH);
        payload = 0;
      }
      else if (receivedChars[2] == 'L')
      {
        digitalWrite(fan, LOW);
        payload = 0;
      }

    }
    // ------- Peristaltic Pump controlls ------ //
    else if (receivedChars[1] == 'U')
    {
      // Activate peristaltic pump #1
      if (receivedChars[2] == '1')
      {
        digitalWrite(p1, HIGH);
        delay(pumpTime);
        digitalWrite(p1, LOW);
        payload = 0;
      }
      // Activate peristaltic pump #2
      else if (receivedChars[2] == '2')
      {
        digitalWrite(p2, HIGH);
        delay(pumpTime);
        digitalWrite(p2, LOW);
        payload = 0;
      }
      // Activate peristaltic pump #3
      else if (receivedChars[2] == '3')
      {
        digitalWrite(p3, HIGH);
        delay(pumpTime);
        digitalWrite(p3, LOW);
        payload = 0;
      }
    }
  }
    // Send out data through Serial
    Serial.println(payload, 3);
}
