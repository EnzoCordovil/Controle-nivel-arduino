#include "Arduino.h"
#include "EEPROM.h"
#include <cassert>
#include <iostream>
uint32_t agora=0; int pins[20]; int saidas[20]; SerialMock Serial; Memoria EEPROM;
#include "../ControleNivel/ControleNivel.ino"
void avancar(uint32_t ms){for(uint32_t i=0;i<ms;i++){agora++;loop();}}
void iniciar(bool inferior=false,bool superior=false,bool apagar=true,uint32_t tempo=0){
 agora=tempo;for(int i=0;i<20;i++){pins[i]=HIGH;saidas[i]=LOW;}
 pins[2]=inferior?LOW:HIGH;pins[3]=superior?LOW:HIGH;
 if(apagar)EEPROM.dado=255;
 setup(); assert(saidas[7]==LOW); avancar(1100);
}
void agua(bool inferior,bool superior){pins[2]=inferior?LOW:HIGH;pins[3]=superior?LOW:HIGH;avancar(150);}
void apertar(){pins[4]=LOW;avancar(60);pins[4]=HIGH;avancar(60);avancar(1100);}
int main(){
 iniciar();assert(saidas[7]==HIGH); // vazio inicia apenas depois da partida
 agua(true,false);avancar(1000);assert(saidas[7]==HIGH);
 agua(true,true);assert(saidas[7]==LOW);
 agua(true,false);assert(saidas[7]==LOW);agua(false,false);assert(saidas[7]==HIGH);
 iniciar(true,false);assert(saidas[7]==LOW); // partida entre niveis aguarda
 iniciar(true,true);assert(saidas[7]==LOW);
 iniciar(false,true);assert(saidas[7]==LOW);assert(EEPROM.dado==0xA5);
 agua(false,false);assert(saidas[7]==LOW);apertar();assert(saidas[7]==HIGH);
 iniciar();avancar(35100);assert(saidas[7]==LOW);assert(EEPROM.dado==0xA5);
 iniciar(false,false,false);assert(saidas[7]==LOW);apertar();assert(saidas[7]==HIGH);
 iniciar();agua(true,false);avancar(35100);assert(saidas[7]==LOW);
 iniciar();agua(true,false);avancar(20000);agua(false,false);agua(true,false);avancar(15100);assert(saidas[7]==LOW); // nao reinicia prazo
 iniciar();agua(false,true);assert(saidas[7]==LOW);assert(EEPROM.dado==0xA5);
 iniciar();pins[3]=LOW;loop();assert(saidas[7]==LOW); // superior corta antes de filtragem
 iniciar();pins[2]=LOW;avancar(10);pins[2]=HIGH;avancar(35200);assert(saidas[7]==LOW); // ruido nao confirma inferior
 iniciar(false,false,true,0xFFFFFF00u);assert(saidas[7]==HIGH);agua(true,false);avancar(35100);assert(saidas[7]==LOW);
 iniciar();pins[4]=LOW;avancar(60);avancar(35100);assert(saidas[7]==LOW);avancar(1000);assert(saidas[7]==LOW); // botao preso nao rearma
 pins[4]=HIGH;avancar(60);apertar();assert(saidas[7]==HIGH);
 iniciar(false,true);apertar();assert(saidas[7]==LOW); // inconsistencia impede rearme
 iniciar();pins[5]=LOW;loop();assert(saidas[7]==LOW&&EEPROM.dado==0xA5);apertar();assert(saidas[7]==LOW);
 pins[5]=HIGH;avancar(150);apertar();assert(saidas[7]==HIGH);
 iniciar();pins[5]=LOW;loop();pins[5]=HIGH;avancar(150);assert(saidas[7]==LOW&&EEPROM.dado==0xA5);
 std::cout<<"PASS: emergencia imediata e rearme, ciclos, partida, 2 timeouts, prioridade superior, ruido, rearme, EEPROM, millis rollover\n";
}
