#include "morseErrorIndication.h"
#include <Arduino.h>

const int DOT_DURATION = 200;
const int DASH_DURATION = 3 * DOT_DURATION;
const int LETTER_SPACE_DURATION = 3 * DOT_DURATION;
const int WORD_SPACE_DURATION = 7 * DOT_DURATION;

const char *morseCode[] = {
    ".-",    // A
    "-...",  // B
    "-.-.",  // C
    "-..",   // D
    ".",     // E
    "..-.",  // F
    "--.",   // G
    "....",  // H
    "..",    // I
    ".---",  // J
    "-.-",   // K
    ".-..",  // L
    "--",    // M
    "-.",    // N
    "---",   // O
    ".--.",  // P
    "--.-",  // Q
    ".-.",   // R
    "...",   // S
    "-",     // T
    "..-",   // U
    "...-",  // V
    ".--",   // W
    "-..-",  // X
    "-.--",  // Y
    "--.."   // Z
    "-----", // 0
    ".----", // 1
    "..---", // 2
    "...--", // 3
    "....-", // 4
    ".....", // 5
    "-....", // 6
    "--...", // 7
    "---..", // 8
    "----."  // 9
};

MorseErrorIndication::MorseErrorIndication(int buzzerPin, int redLedPin, int yellowLedPin)
{
    _buzzerPin = buzzerPin;
    _redLedPin = redLedPin;
    _yellowLedPin = yellowLedPin;
    pinMode(_buzzerPin, OUTPUT);
    pinMode(_redLedPin, OUTPUT);
    pinMode(_yellowLedPin, OUTPUT);
}

/*
 * MorseErrorIndication class methods
 */

/*
 * Buzzes the Morse code for the given error code and blinks an LED
 */
void MorseErrorIndication::buzzMorseCodeWithError(const char *errorCode, int toneFrequency, int ledPin)
{
    for (int i = 0; errorCode[i] != '\0'; i++)
    {
        buzzMorseSymbol(errorCode[i], toneFrequency);
        blinkMorseSymbol(errorCode[i], ledPin);
        delay(DOT_DURATION); // Adjust this delay if needed
    }
    delay(LETTER_SPACE_DURATION);
}

/*
 * Buzzes the Morse code for the given error string and blinks an LED
 *
 * The error string should be a sequence of error codes separated by 'S'
 * and terminated by 'Z' (e.g. "ABSCDSZ")
 */
void MorseErrorIndication::buzzMorseStringWithError(const char *errorString, int toneFrequency, int ledPin)
{
    for (int i = 0; errorString[i] != '\0'; i++)
    {
        if (errorString[i] == 'S')
        {
            delay(WORD_SPACE_DURATION); // Pause between errors
        }
        else
        {
            buzzMorseCodeWithError(&errorString[i], toneFrequency, ledPin);
            // Skip to the end of the current error code
            while (errorString[i] != 'S' && errorString[i] != '\0')
            {
                i++;
            }
            i--; // Decrement i to account for the loop increment
        }
    }
}

/*
 * Buzzes a Morse symbol, either a dot or a dash
 */
void MorseErrorIndication::buzzMorseSymbol(char symbol, int toneFrequency)
{
    if (symbol == '.')
    {
        buzzerDot(toneFrequency);
    }
    else if (symbol == '-')
    {
        buzzerDash(toneFrequency);
    }
}

/*
 * Buzzes a dot
 */
void MorseErrorIndication::buzzerDot(int toneFrequency)
{
    if (millis() - _lastBuzzTime >= DOT_DURATION)
    {
        tone(_buzzerPin, toneFrequency);
        _lastBuzzTime = millis();
    }
    else if (millis() - _lastBuzzTime >= DOT_DURATION / 2)
    {
        noTone(_buzzerPin);
    }
}

/*
 * Buzzes a dash
 */
void MorseErrorIndication::buzzerDash(int toneFrequency)
{
    if (millis() - _lastBuzzTime >= DASH_DURATION)
    {
        tone(_buzzerPin, toneFrequency);
        _lastBuzzTime = millis();
    }
    else if (millis() - _lastBuzzTime >= DASH_DURATION / 2)
    {
        noTone(_buzzerPin);
    }
}

/*
 * Blinks a Morse symbol, either a dot or a dash
 */
void MorseErrorIndication::blinkMorseSymbol(char symbol, int ledPin)
{
    if (symbol == '.')
    {
        blinkDot(ledPin);
    }
    else if (symbol == '-')
    {
        blinkDash(ledPin);
    }
}

/*
 * Blinks a dot
 */
void MorseErrorIndication::blinkDot(int ledPin)
{
    if (millis() - _lastBlinkTime >= DOT_DURATION)
    {
        digitalWrite(ledPin, HIGH);
        _lastBlinkTime = millis();
    }
    else if (millis() - _lastBlinkTime >= DOT_DURATION / 2)
    {
        digitalWrite(ledPin, LOW);
    }
}

/*
 * Blinks a dash
 */
void MorseErrorIndication::blinkDash(int ledPin)
{
    if (millis() - _lastBlinkTime >= DASH_DURATION)
    {
        digitalWrite(ledPin, HIGH);
        _lastBlinkTime = millis();
    }
    else if (millis() - _lastBlinkTime >= DASH_DURATION / 2)
    {
        digitalWrite(ledPin, LOW);
    }
}
