#include "Arduino.h"
#include "EEPROM.h"
#include <cassert>
#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
uint32_t agora=0; int pins[20]; int saidas[20]; SerialMock Serial; Memoria EEPROM;
#include "../ControleNivel/ControleNivel.ino"
struct Tanque {
 double volume=0, entrada=6, retirada=0, maximo=0;
 double atrasoFechamento=300, atrasoRestante=0;
 int defeitoInf=0,defeitoSup=0,defeitoEmerg=0;
 bool valvulaTravada=false, extravasorObstruido=false; int comandoAnterior=LOW;
 // Modelo preliminar de tubo vertical aberto de 50 mm internos.
 // Geometria de exemplo: 200 x 125 mm internos.
 // Acima da crista nao ha mais tubo vertical ocupando a secao do tanque.
 double descarga(){
  if(extravasorObstruido)return 0;
  const double h=std::max(0.0,(volume-2.8)/1000.0/(.200*.125));
  const double q=(2.0/3.0)*.4*3.141592653589793*.05*std::sqrt(2*9.81)*std::pow(h,1.5);
  return std::min(q*60000.0,18.0); // L/min: capacidade de conducao ASSUMIDA
 }
 void sinais(){
  pins[2]=(defeitoInf==2 || (defeitoInf==0 && volume>=1))?LOW:HIGH;
  pins[3]=(defeitoSup==2 || (defeitoSup==0 && volume>=2))?LOW:HIGH;
  pins[5]=(defeitoEmerg==2 || (defeitoEmerg==0 && volume>=2.5))?LOW:HIGH;
 }
 void ligar(bool limpar=true){
  agora=0;for(int i=0;i<20;i++){pins[i]=HIGH;saidas[i]=LOW;}
  if(limpar)EEPROM.dado=255;
  sinais();setup();maximo=volume;comandoAnterior=LOW;atrasoRestante=0;
 }
 void rodar(uint32_t ms){
  for(uint32_t i=0;i<ms;i++){
   if(comandoAnterior==HIGH && saidas[7]==LOW)atrasoRestante=atrasoFechamento;
   comandoAnterior=saidas[7];
   const bool aberta=saidas[7]==HIGH || atrasoRestante>0 || valvulaTravada;
   if(atrasoRestante>0)atrasoRestante--;
   volume+=((aberta?entrada:0)-retirada-descarga())/60000.0;
   if(volume<0)volume=0;
   if(volume>maximo)maximo=volume;
   sinais();++agora;loop();
  }
 }
};
int casos=0;
void relatar(const char* nome,Tanque& t){
 std::cout<<"PASS | "<<nome<<" | volume="<<std::fixed<<std::setprecision(3)<<t.volume
 <<" L | max="<<t.maximo<<" L | bloqueado="<<(EEPROM.dado==0xA5)<<"\n";casos++;
}
int main(){
 {Tanque t;t.ligar();t.rodar(150000);assert(t.volume>=2&&t.volume<2.04&&saidas[7]==LOW&&EEPROM.dado!=0xA5);relatar("normal 6 L/min",t);}
 {Tanque t;t.entrada=3;t.ligar();t.rodar(150000);assert(t.volume>=2&&t.volume<2.02&&EEPROM.dado!=0xA5);relatar("vazao menor: 3 L/min",t);}
 {Tanque t;t.entrada=3;t.retirada=1;t.ligar();t.rodar(125000);assert(EEPROM.dado!=0xA5&&t.maximo>=2&&t.maximo<2.03);relatar("entrada 3, saida 1 L/min: liquida 2",t);}
 {Tanque t;t.retirada=1;t.ligar();t.rodar(600000);assert(EEPROM.dado!=0xA5&&t.maximo>=2&&t.maximo<2.04);relatar("10 minutos com retirada simultanea",t);}
 {Tanque t;t.defeitoSup=1;t.ligar();t.rodar(150000);assert(t.maximo>=2.5&&t.maximo<2.54&&saidas[7]==LOW&&EEPROM.dado==0xA5);relatar("superior seco: emergencia 6 L/min",t);}
 {Tanque t;t.entrada=12;t.defeitoSup=1;t.ligar();t.rodar(150000);assert(t.maximo>=2.5&&t.maximo<2.57&&saidas[7]==LOW&&EEPROM.dado==0xA5);relatar("superior seco: emergencia 12 L/min",t);}
 {Tanque t;t.entrada=12;t.defeitoInf=1;t.defeitoSup=1;t.ligar();t.rodar(150000);assert(t.maximo<2.57&&EEPROM.dado==0xA5);relatar("inferior e superior secos, emergencia funcional",t);}
 {Tanque t;t.defeitoInf=1;t.ligar();t.rodar(150000);assert(t.maximo<2.05&&EEPROM.dado==0xA5);relatar("inferior seco: inconsistencia no superior",t);}
 {Tanque t;t.defeitoEmerg=1;t.ligar();t.rodar(150000);assert(t.maximo<2.04&&EEPROM.dado!=0xA5);relatar("emergencia seca: superior normal encerra",t);}
 {Tanque t;t.defeitoEmerg=2;t.ligar();t.rodar(5000);assert(t.volume==0&&EEPROM.dado==0xA5);relatar("emergencia ativa na partida bloqueia",t);}
 {Tanque t;t.entrada=0;t.ligar();t.rodar(70000);assert(t.volume==0&&EEPROM.dado==0xA5);relatar("falta de agua: timeout",t);}
 {Tanque t;t.defeitoInf=2;t.ligar();t.rodar(150000);assert(t.volume==0&&EEPROM.dado!=0xA5);relatar("LIMITE: inferior preso molhado sem diagnostico",t);}
 {Tanque t;t.entrada=12;t.defeitoSup=1;t.defeitoEmerg=1;t.ligar();t.rodar(150000);assert(t.maximo<4&&EEPROM.dado==0xA5);relatar("superior e emergencia secos: extravasor funcional",t);}
 {Tanque t;t.valvulaTravada=true;t.ligar();t.rodar(70000);assert(t.maximo<4&&EEPROM.dado==0xA5&&saidas[7]==LOW);relatar("valvula travada: extravasor funcional",t);}
 {Tanque t;t.defeitoEmerg=2;t.ligar();t.rodar(10);assert(EEPROM.dado==0xA5);t.defeitoEmerg=0;t.ligar(false);t.rodar(2000);assert(saidas[7]==LOW&&EEPROM.dado==0xA5);relatar("bloqueio persistente",t);}
 {Tanque t;t.ligar();for(int c=0;c<10;c++){t.volume=.9;t.rodar(150000);assert(t.volume>=2&&t.volume<2.04&&EEPROM.dado!=0xA5);}relatar("dez ciclos completos",t);}
 {Tanque t;t.valvulaTravada=true;t.entrada=12;t.ligar();t.rodar(180000);assert(t.maximo<4&&EEPROM.dado==0xA5);relatar("valvula travada a 12 L/min, extravasor ativo",t);}
 {Tanque t;t.valvulaTravada=true;t.extravasorObstruido=true;t.entrada=12;t.ligar();t.rodar(30000);assert(t.maximo>5);relatar("LIMITE: valvula travada e extravasor obstruido",t);}
 int varredura=0;
 for(int q=3;q<=12;q++)for(int n=0;n<=20;n++){
  Tanque t;t.entrada=q;t.volume=n/10.0;t.ligar();t.rodar(150000);
  assert(t.maximo<2.07&&EEPROM.dado!=0xA5);
  if(n<10)assert(t.volume>=2&&t.volume<2.07);
  else assert(std::abs(t.volume-n/10.0)<0.001);
  varredura++;
 }
 std::cout<<"PASS | "<<varredura<<" combinacoes de vazao e volume inicial\n";
 std::cout<<"TOTAL: "<<casos<<" cenarios explicitos + "<<varredura<<" combinacoes\n";
}
