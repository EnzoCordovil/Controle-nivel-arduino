#pragma once
#include <stdint.h>
struct Memoria { uint8_t dado=255; uint8_t read(int){return dado;} void update(int,uint8_t x){dado=x;} };
extern Memoria EEPROM;
