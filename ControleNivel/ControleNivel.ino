/*
  Projeto de Controle Automatico de Nivel de Agua - Arduino Uno R3
  Sensores: 3 x SEN0485, ativos em LOW, alimentados em 5 V.
  Rele: DFR0017, comando ativo em HIGH. Contatos COM/NO.
  D2 = inferior (~1 L), D3 = superior (~2 L), D7 = rele.
  D5 = emergencia (~2,5 L), ativa em LOW.
  D4 = botao momentaneo normalmente aberto para GND (INPUT_PULLUP).
  D13 = LED integrado: aceso durante bloqueio.

  Hardware: resistor de 10 kohms entre comando do rele e GND;
  diodo 1N4001 em paralelo com a valvula (faixa no positivo).
  A valvula recebe 12 V pelos contatos; nunca por um pino do Uno.

  Supervisao de 35 s por etapa: 1 L a vazao liquida minima de 2 L/min
  leva 30 s, mais 5 s de margem. Corte normal em ~2 L; emergencia em ~2,5 L.
  Nao medem vazao e nao garantem protecao contra todas as falhas.
  Uma falha fica gravada no byte 0 da EEPROM ate rearme manual.
  Serial: 9600 baud. Sem bibliotecas externas.
*/
#include <Arduino.h>
#include <EEPROM.h>

const uint8_t PIN_INFERIOR = 2;
const uint8_t PIN_SUPERIOR = 3;
const uint8_t PIN_REARME = 4;
const uint8_t PIN_EMERGENCIA = 5;
const uint8_t PIN_RELE = 7;
const uint8_t PIN_FALHA = LED_BUILTIN;
const uint32_t PARTIDA_MS = 1000UL;
const uint32_t FILTRO_SENSOR_MS = 100UL;
const uint32_t FILTRO_BOTAO_MS = 40UL;
const uint32_t PRAZO_INFERIOR_MS = 35000UL;
const uint32_t PRAZO_SUPERIOR_MS = 35000UL;
const int ENDERECO_FALHA = 0;
const uint8_t MARCA_FALHA = 0xA5;
const uint8_t MARCA_LIBERADO = 0x00;

enum class Estado : uint8_t {
  INICIALIZANDO, AGUARDANDO, ATE_INFERIOR, ATE_SUPERIOR, BLOQUEADO
};

// Subtracao sem sinal permite atravessar o retorno de millis() a zero.
bool expirou(uint32_t agora, uint32_t inicio, uint32_t prazo) {
  return uint32_t(agora - inicio) >= prazo;
}

struct EntradaFiltrada {
  bool bruta;
  bool estavel;
  uint32_t mudouEm;

  void iniciar(bool valor, uint32_t agora) {
    bruta = valor;
    estavel = valor;
    mudouEm = agora;
  }
  void atualizar(bool valor, uint32_t agora, uint32_t filtro) {
    if (valor != bruta) {
      bruta = valor;
      mudouEm = agora;
    }
    if (expirou(agora, mudouEm, filtro)) estavel = bruta;
  }
};

Estado estado = Estado::INICIALIZANDO;
EntradaFiltrada inferior, superior, emergencia, botao;
uint32_t inicioEtapa = 0;
bool rearmeArmado = false;
bool botaoAnterior = false;

void bloquear(const char* motivo) {
  digitalWrite(PIN_RELE, LOW);
  estado = Estado::BLOQUEADO;
  rearmeArmado = false;
  EEPROM.update(ENDERECO_FALHA, MARCA_FALHA);
  Serial.println(motivo);
}

void mudarEtapa(Estado proximo, uint32_t agora) {
  estado = proximo;
  inicioEtapa = agora;
}

void setup() {
  // Preparar latch LOW antes de tornar o pino uma saida.
  digitalWrite(PIN_RELE, LOW);
  pinMode(PIN_RELE, OUTPUT);
  pinMode(PIN_FALHA, OUTPUT);
  pinMode(PIN_INFERIOR, INPUT_PULLUP);
  pinMode(PIN_SUPERIOR, INPUT_PULLUP);
  pinMode(PIN_EMERGENCIA, INPUT_PULLUP);
  pinMode(PIN_REARME, INPUT_PULLUP);
  Serial.begin(9600);

  uint32_t agora = uint32_t(millis());
  inferior.iniciar(digitalRead(PIN_INFERIOR) == LOW, agora);
  superior.iniciar(digitalRead(PIN_SUPERIOR) == LOW, agora);
  emergencia.iniciar(digitalRead(PIN_EMERGENCIA) == LOW, agora);
  botao.iniciar(digitalRead(PIN_REARME) == LOW, agora);
  botaoAnterior = botao.estavel;
  rearmeArmado = false;
  inicioEtapa = agora;
  uint8_t memoria = EEPROM.read(ENDERECO_FALHA);
  // EEPROM apagada (0xFF): primeira utilizacao. Outros valores: bloquear.
  estado = (memoria == MARCA_LIBERADO || memoria == 0xFF)
      ? Estado::INICIALIZANDO : Estado::BLOQUEADO;
  digitalWrite(PIN_FALHA, estado == Estado::BLOQUEADO ? HIGH : LOW);
  Serial.println(estado == Estado::BLOQUEADO
      ? F("Bloqueio registrado. Corrigir causa e rearmar.")
      : F("Inicializando com valvula fechada."));
}

void loop() {
  const uint32_t agora = uint32_t(millis());
  inferior.atualizar(digitalRead(PIN_INFERIOR) == LOW, agora, FILTRO_SENSOR_MS);
  superior.atualizar(digitalRead(PIN_SUPERIOR) == LOW, agora, FILTRO_SENSOR_MS);
  emergencia.atualizar(digitalRead(PIN_EMERGENCIA) == LOW, agora, FILTRO_SENSOR_MS);
  botao.atualizar(digitalRead(PIN_REARME) == LOW, agora, FILTRO_BOTAO_MS);
  const bool apertou = botao.estavel && !botaoAnterior;
  botaoAnterior = botao.estavel;
  const bool incoerente = superior.estavel && !inferior.estavel;
  const bool estabilizados =
      expirou(agora, inferior.mudouEm, FILTRO_SENSOR_MS) &&
      expirou(agora, superior.mudouEm, FILTRO_SENSOR_MS) &&
      expirou(agora, emergencia.mudouEm, FILTRO_SENSOR_MS);

  // Emergencia tem prioridade absoluta, inclusive durante a partida.
  // Um pulso pode bloquear: rearme manual depois de inspecionar.
  if (emergencia.bruta && estado != Estado::BLOQUEADO) {
    bloquear("Falha: nivel de emergencia detectado.");
  }

  if (estado == Estado::BLOQUEADO) {
    // Exige soltar apos a falha e depois uma NOVA pressao.
    if (!botao.estavel && !botao.bruta) rearmeArmado = true;
    if (apertou && rearmeArmado) {
      rearmeArmado = false;
      if (estabilizados && !incoerente && !emergencia.bruta && !emergencia.estavel) {
        EEPROM.update(ENDERECO_FALHA, MARCA_LIBERADO);
        mudarEtapa(Estado::INICIALIZANDO, agora);
        Serial.println(F("Rearme aceito. Verificando sensores."));
      } else {
        Serial.println(F("Rearme recusado: verificar sensores."));
      }
    }
  } else if (estado == Estado::INICIALIZANDO) {
    if (expirou(agora, inicioEtapa, PARTIDA_MS) && estabilizados) {
      if (incoerente) {
        bloquear("Falha: superior com agua e inferior seco.");
      } else if (!inferior.estavel && !superior.estavel) {
        mudarEtapa(Estado::ATE_INFERIOR, agora);
        Serial.println(F("Enchendo ate o sensor inferior."));
      } else {
        estado = Estado::AGUARDANDO;
      }
    }
  } else if (incoerente) {
    bloquear("Falha: superior com agua e inferior seco.");
  } else if (superior.estavel) {
    // Prioridade ao nivel superior em qualquer etapa de enchimento.
    if (estado != Estado::AGUARDANDO) Serial.println(F("Nivel superior: fechamento."));
    estado = Estado::AGUARDANDO;
  } else {
    switch (estado) {
      case Estado::AGUARDANDO:
        if (!inferior.estavel) {
          mudarEtapa(Estado::ATE_INFERIOR, agora);
          Serial.println(F("Reposicao iniciada."));
        }
        break;
      case Estado::ATE_INFERIOR:
        if (inferior.estavel) {
          mudarEtapa(Estado::ATE_SUPERIOR, agora);
          Serial.println(F("Inferior detectado. Segundo prazo iniciado."));
        } else if (expirou(agora, inicioEtapa, PRAZO_INFERIOR_MS)) {
          bloquear("Falha: prazo para sensor inferior excedido.");
        }
        break;
      case Estado::ATE_SUPERIOR:
        // Nao reiniciar a contagem se o inferior oscilar ou voltar a seco.
        if (expirou(agora, inicioEtapa, PRAZO_SUPERIOR_MS)) {
          bloquear("Falha: prazo para sensor superior excedido.");
        }
        break;
      default:
        break;
    }
  }

  const bool enchendo = estado == Estado::ATE_INFERIOR || estado == Estado::ATE_SUPERIOR;
  // Corte imediato no sinal bruto do superior; filtro confirma fim/falha.
  digitalWrite(PIN_RELE, enchendo && !superior.bruta && !emergencia.bruta ? HIGH : LOW);
  digitalWrite(PIN_FALHA, estado == Estado::BLOQUEADO ? HIGH : LOW);
}
