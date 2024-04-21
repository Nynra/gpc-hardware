/*
 * Arduino for monitoring the GPC power and some other stuff
 */
#include <Arduino.h>
#include <Wire.h>
#include <morseErrorIndication.h>
#include <SimpleCLI.h>
#include <Command.h>

// Some global variables
const bool DEBUG = false;
const int BAUD_RATE = 9600;  // Only used if DEBUG is true
const int I2C_ADDRESS = 15;

/*
 * Pin definitions
 */
// Digital pin definitions
const int RPI_RELAY_PIN = 3;
const int TEENSY_RELAY_PIN = 4;
const int ESP32_RELAY_PIN = 5;

const int CASE_INTRUSION_PIN = 6;
const int BUZZER_PIN = 7;

const int YELLOW_LED_PIN = 9;
const int RED_LED_PIN = 10;

// Analog pin definitions
const int TEMP_SENSOR_PIN = A0;
const int FIRE_SENSOR_PIN = A1;

const int RPI_POWER_MON_PIN = A2;
const int TEENSY_POWER_MON_PIN = A3;
const int ESP32_POWER_MON_PIN = A4;
const int ARDUINO_POWER_MON_PIN = A5;

/*
 * State and threshold definitions
 */
// Relays
bool RPI_RELAY_STATE = false;
bool LAST_RPI_RELAY_STATE = false;

bool TEENSY_RELAY_STATE = false;
bool LAST_TEENSY_RELAY_STATE = false;

bool ESP32_RELAY_STATE = false;
bool LAST_ESP32_RELAY_STATE = false;

// Sensors
int TEMP_SENSOR_THRESHOLD = 30;
int FIRE_SENSOR_THRESHOLD = 100;

// Power Monitors
int GENERAL_POWER_MON_THRESHOLD = 80; // % of the power

float RPI_POWER_MON_DIV_FACTOR = 1; // 1 if no divider is used
float RPI_POWER_MON_VALUE = 0;
int RPI_POWER_MON_THRESHOLD = GENERAL_POWER_MON_THRESHOLD;

float TEENSY_POWER_MON_DIV_FACTOR = 0.6; // 3.3V / 5V approx 0.6
float TEENSY_POWER_MON_VALUE = 0;
int TEENSY_POWER_MON_THRESHOLD = GENERAL_POWER_MON_THRESHOLD;

float ESP32_POWER_MON_DIV_FACTOR = 0.6;
float ESP32_POWER_MON_VALUE = 0;
int ESP32_POWER_MON_THRESHOLD = GENERAL_POWER_MON_THRESHOLD;

float ARDUINO_POWER_MON_DIV_FACTOR = 1;
float ARDUINO_POWER_MON_VALUE = 0;
int ARDUINO_POWER_MON_THRESHOLD = GENERAL_POWER_MON_THRESHOLD;

// Error states (Yellow LED)
bool RPI_POWER_MON_ERROR_STATE = false;
bool TEENSY_POWER_MON_ERROR_STATE = false;
bool ESP32_POWER_MON_ERROR_STATE = false;
bool ARDUINO_POWER_MON_ERROR_STATE = false;

// Emergency states (Red LED, power cut and buzzer on)
bool CASE_INTRUSION_ERROR_STATE = false;
bool TEMP_SENSOR_ERROR_STATE = false;
bool FIRE_SENSOR_ERROR_STATE = false;

char RPI_POWER_ERROR_CODE = 'R';
char TEENSY_POWER_ERROR_CODE = 'T';
char ESP32_POWER_ERROR_CODE = 'E';
char ARDUINO_POWER_ERROR_CODE = 'A';
char INTRUSION_ERROR_CODE = 'I';
char TEMPERATURE_ERROR_CODE = 'T';
char FIRE_ERROR_CODE = 'F';

const int NUM_ERROR_FLAGS = 7;

// Function prototypes
void updateRelays();
void updatePowerMonitors();
void updateErrorStates();
void indicateErrors();
String buildErrorString(bool *errorFlags, int numFlags);
void switchRelayCallback(int numBytes);
void getErrorsCallback();


// Create some objects
MorseErrorIndication errorIndication(BUZZER_PIN, RED_LED_PIN, YELLOW_LED_PIN);


void setup()
{
  // Set the output pins
  pinMode(RPI_RELAY_PIN, OUTPUT);
  pinMode(TEENSY_RELAY_PIN, OUTPUT);
  pinMode(ESP32_RELAY_PIN, OUTPUT);
  pinMode(YELLOW_LED_PIN, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);

  // Set the input pins
  pinMode(CASE_INTRUSION_PIN, INPUT);

  // Set the I2C address
  Wire.begin(I2C_ADDRESS);
  Wire.onReceive(switchRelayCallback);
  Wire.onRequest(getErrorsCallback);

  if (DEBUG)
  {
    Serial.begin(BAUD_RATE);
  }
}

void loop()
{
  // Run the update functions
  updateRelays();
  updatePowerMonitors();
  updateErrorStates();

  // Indicate the errors
  indicateErrors();
}

/*
 * Updating methods
 */

// Update the relay states
void updateRelays()
{
  // Update the RPI relay
  if (RPI_RELAY_STATE != LAST_RPI_RELAY_STATE)
  {
    digitalWrite(RPI_RELAY_PIN, RPI_RELAY_STATE);
    LAST_RPI_RELAY_STATE = RPI_RELAY_STATE;
  }

  // Update the Teensy relay
  if (TEENSY_RELAY_STATE != LAST_TEENSY_RELAY_STATE)
  {
    digitalWrite(TEENSY_RELAY_PIN, TEENSY_RELAY_STATE);
    LAST_TEENSY_RELAY_STATE = TEENSY_RELAY_STATE;
  }

  // Update the ESP32 relay
  if (ESP32_RELAY_STATE != LAST_ESP32_RELAY_STATE)
  {
    digitalWrite(ESP32_RELAY_PIN, ESP32_RELAY_STATE);
    LAST_ESP32_RELAY_STATE = ESP32_RELAY_STATE;
  }
}

// Update the power monitor values
void updatePowerMonitors()
{
  // Read the RPI power monitor value
  RPI_POWER_MON_VALUE = analogRead(RPI_POWER_MON_PIN) / RPI_POWER_MON_DIV_FACTOR;

  // Read the Teensy power monitor value
  TEENSY_POWER_MON_VALUE = analogRead(TEENSY_POWER_MON_PIN) / TEENSY_POWER_MON_DIV_FACTOR;

  // Read the ESP32 power monitor value
  ESP32_POWER_MON_VALUE = analogRead(ESP32_POWER_MON_PIN) / ESP32_POWER_MON_DIV_FACTOR;

  // Read the Arduino power monitor value
  ARDUINO_POWER_MON_VALUE = analogRead(ARDUINO_POWER_MON_PIN) / ARDUINO_POWER_MON_DIV_FACTOR;
}

// Update the error states
void updateErrorStates()
{
  // Update the RPI power monitor error state
  if (RPI_POWER_MON_VALUE > RPI_POWER_MON_THRESHOLD)
  {
    RPI_POWER_MON_ERROR_STATE = true;
  }
  else
  {
    RPI_POWER_MON_ERROR_STATE = false;
  }

  // Update the Teensy power monitor error state
  if (TEENSY_POWER_MON_VALUE > TEENSY_POWER_MON_THRESHOLD)
  {
    TEENSY_POWER_MON_ERROR_STATE = true;
  }
  else
  {
    TEENSY_POWER_MON_ERROR_STATE = false;
  }

  // Update the ESP32 power monitor error state
  if (ESP32_POWER_MON_VALUE > ESP32_POWER_MON_THRESHOLD)
  {
    ESP32_POWER_MON_ERROR_STATE = true;
  }
  else
  {
    ESP32_POWER_MON_ERROR_STATE = false;
  }

  // Update the Arduino power monitor error state
  if (ARDUINO_POWER_MON_VALUE > ARDUINO_POWER_MON_THRESHOLD)
  {
    ARDUINO_POWER_MON_ERROR_STATE = true;
  }
  else
  {
    ARDUINO_POWER_MON_ERROR_STATE = false;
  }

  // Update the case intrusion error state
  if (digitalRead(CASE_INTRUSION_PIN) == HIGH)
  {
    CASE_INTRUSION_ERROR_STATE = true;
  }
  else
  {
    CASE_INTRUSION_ERROR_STATE = false;
  }

  // Update the temperature sensor error state
  if (analogRead(TEMP_SENSOR_PIN) > TEMP_SENSOR_THRESHOLD)
  {
    TEMP_SENSOR_ERROR_STATE = true;
  }
  else
  {
    TEMP_SENSOR_ERROR_STATE = false;
  }

  // Update the fire sensor error state
  if (analogRead(FIRE_SENSOR_PIN) > FIRE_SENSOR_THRESHOLD)
  {
    FIRE_SENSOR_ERROR_STATE = true;
  }
  else
  {
    FIRE_SENSOR_ERROR_STATE = false;
  }
}

/*
 * Error indication methods
 */

// Indicate the errors using Morse code and LEDs
void indicateErrors()
{
  // If the fire error, temperature error, or case intrusion error is present, make an emergency stop
  int led_pin = YELLOW_LED_PIN;
  if (FIRE_SENSOR_ERROR_STATE || TEMP_SENSOR_ERROR_STATE || CASE_INTRUSION_ERROR_STATE)
  {
    // Turn off all relays
    RPI_RELAY_STATE = false;
    TEENSY_RELAY_STATE = false;
    ESP32_RELAY_STATE = false;
    updateRelays();

    // Set the colour to red
    led_pin = RED_LED_PIN;
  }

  // Create an array of error flags
  bool errorFlags[NUM_ERROR_FLAGS] = {
      CASE_INTRUSION_ERROR_STATE,
      TEMP_SENSOR_ERROR_STATE,
      FIRE_SENSOR_ERROR_STATE,
      RPI_POWER_MON_ERROR_STATE,
      TEENSY_POWER_MON_ERROR_STATE,
      ESP32_POWER_MON_ERROR_STATE,
      ARDUINO_POWER_MON_ERROR_STATE};

  // Build the error string from the error flags
  String errorString = buildErrorString(errorFlags, NUM_ERROR_FLAGS);

  // Buzz the error string
  errorIndication.buzzMorseStringWithError(errorString.c_str(), 1000, led_pin);
}

// Build the error string from the error flags
String buildErrorString(bool *errorFlags, int numFlags)
{
  String errorString = "";

  for (int i = 0; i < numFlags; i++)
  {
    if (errorFlags[i])
    {
      // Convert the index to the corresponding error code string
      const char *errorCode;
      switch (i)
      {
      case 0:
        errorCode = &INTRUSION_ERROR_CODE;
        break;
      case 1:
        errorCode = &TEMPERATURE_ERROR_CODE;
        break;
      case 2:
        errorCode = &FIRE_ERROR_CODE;
        break;
      case 3:
        errorCode = &RPI_POWER_ERROR_CODE;
        break;
      case 4:
        errorCode = &TEENSY_POWER_ERROR_CODE;
        break;
      case 5:
        errorCode = &ESP32_POWER_ERROR_CODE;
        break;
      case 6:
        errorCode = &ARDUINO_POWER_ERROR_CODE;
        break;
      // Add more cases for other error conditions if needed
      default:
        // Use default error code character ('A' + index) if not predefined
        errorCode = "A";
      }
      errorString += errorCode;
      errorString += 'S'; // Separate error codes with 'S'
    }
  }

  if (errorString.endsWith("S"))
  {
    // Remove the trailing 'S' if present
    errorString.remove(errorString.length() - 1);
  }

  return errorString;
}

/*
 * I2C Callbacks
 */

// Callback for the switchRelay command
void switchRelayCallback(int numBytes)
{
  // Read the command byte
  byte command = Wire.read();

  // The relay index is the first byte of the command, and the relay state is the second byte
  int relayIndex = command & 0b00000011;
  bool relayState = command & 0b00000100;

  switch (relayIndex)
  {
  case 0:
    RPI_RELAY_STATE = relayState;
    break;
  case 1:
    TEENSY_RELAY_STATE = relayState;
    break;
  case 2:
    ESP32_RELAY_STATE = relayState;
    break;
  default:
    break;
  }
}

// Callback for the getErrors command
void getErrorsCallback()
{
  // Create a byte array to store the error flags
  byte errorFlags[NUM_ERROR_FLAGS] = {
      CASE_INTRUSION_ERROR_STATE,
      TEMP_SENSOR_ERROR_STATE,
      FIRE_SENSOR_ERROR_STATE,
      RPI_POWER_MON_ERROR_STATE,
      TEENSY_POWER_MON_ERROR_STATE,
      ESP32_POWER_MON_ERROR_STATE,
      ARDUINO_POWER_MON_ERROR_STATE};

  // Send the error flags
  Wire.write(errorFlags, NUM_ERROR_FLAGS);
}