#ifndef MORSE_ERROR_INDICATION_H
#define MORSE_ERROR_INDICATION_H

#include <Arduino.h>

extern const int DOT_DURATION;
extern const int DASH_DURATION;
extern const int LETTER_SPACE_DURATION;
extern const int WORD_SPACE_DURATION;

class MorseErrorIndication
{
public:
    MorseErrorIndication(int buzzerPin, int redLedPin, int yellowLedPin);
    void buzzMorseCodeWithError(const char *errorCode, int toneFrequency, int ledPin);
    void buzzMorseStringWithError(const char *errorString, int toneFrequency, int ledPin);

private:
    void buzzMorseSymbol(char symbol, int toneFrequency);
    void buzzerDot(int toneFrequency);
    void buzzerDash(int toneFrequency);
    void blinkMorseSymbol(char symbol, int ledPin);
    void blinkDot(int ledPin);
    void blinkDash(int ledPin);

    int _buzzerPin;
    int _redLedPin;
    int _yellowLedPin;
    int _currentSymbolIndex;
    unsigned long _lastBuzzTime;
    unsigned long _lastBlinkTime;
};

#endif
