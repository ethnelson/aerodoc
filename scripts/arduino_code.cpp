boolean newData = false;
const byte numChars = 32;
char receivedChars[numChars];
float payload = -1;

// -------------------------------------------------------------------------- //
//                               PIN MAPPING                                  //
// -------------------------------------------------------------------------- //
// ------------------------------ sensor pins ------------------------------- //
int ec = 0;
int ph = 0;
int temp = 0;
int hum = 0;
int wat = 0;
// --------------------------- controller pins ------------------------------ //
int light = 0;
int fan = 0;
int p1 = 0;
int p2 = 0;
int p3 = 0;

void setup() {
  Serial.begin(9600);
  // Don't forget about pinModes
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

void handshake()
{
  while (Serial.available() <= 0)
  {
    Serial.print('S');
    delay(300);
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
    if (receivedChars[1] == 'E')
    {
      //Read EC Sensor
    }
    else if (receivedChars[1] == 'P')
    {
      //Read PH Sensor
    }
    else if (receivedChars[1] == 'T')
    {
      //Read Temperature Sensor
    }
    else if (receivedChars[1] == 'H')
    {
      //Read Humidity Sensor
    }
    else if (receivedChars[1] == 'W')
    {
      // Water level sensor
      payload = analogRead(wat);
    }
  }
    // ------------------------- CONTROLLER SECTION ------------------------- //
    // L - control the lights (on/off)
    // F - control the fan (on/off)
    // U - Peristaltic pump control
    //    1 - pump #1
    //    etc ..
    //
    // When specifying the action for the control (on/off) 'H' and 'L' are used to
    // specify if the voltage is HIGH or LOW
  else if (receivedChars[0] == 'C')
  {
    if (receivedChars[1] == 'L')
    {
      // Light control
      if (receivedChars[2] == 'H')
      {
        digitalWrite(light, HIGH);
      }
      else if (receivedChars[2] == 'L')
      {
        digitalWrite(light, LOW);
      }
    }
    else if (receivedChars[1] == 'F')
    {
      // Fan Control
      if (receivedChars[2] == 'H')
      {
        digitalWrite(fan, HIGH);
      }
      else if (receivedChars[2] == 'L')
      {
        digitalWrite(fan, LOW);
      }

    }
    // ------- Peristaltic Pump controlls ------ //
    else if (receivedChars[1] == 'U')
    {
      // Do peristaltic pump controll
      if (receivedChars[2] == '1')
      {
        // activate peristaltic pump #1
      }
      else if (receivedChars[2] == '2')
      {
        // activate peristaltic pump #2
      }
      else if (receivedChars[2] == '3')
      {
        // activate peristaltic pump #3
      }
    }
  }
    // Send out data through Serial
    Serial.println(payload, 3);
}
