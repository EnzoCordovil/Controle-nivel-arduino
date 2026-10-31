#pragma once
#include <stdint.h>
#include <stddef.h>
#define HIGH 1
#define LOW 0
#define INPUT_PULLUP 2
#define OUTPUT 1
#define LED_BUILTIN 13
#define F(x) x
extern uint32_t agora;
extern int pins[20];
extern int saidas[20];
inline unsigned long millis(){return agora;}
inline int digitalRead(int p){return pins[p];}
inline void digitalWrite(int p,int v){saidas[p]=v;}
inline void pinMode(int,int){}
struct SerialMock{void begin(int){} template<class T> void println(T){} };
extern SerialMock Serial;
