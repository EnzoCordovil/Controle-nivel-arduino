# Dimensionamento elétrico

[English](en/ELECTRICAL_DESIGN.md) | [Português](DIMENSIONAMENTO_ELETRICO.md)

Esta configuração de referência completa o circuito de controle já desenhado. Os valores de catálogo estão separados das reservas de cálculo. A seleção não representa medições de uma montagem.

## Componentes e condições

| Elemento | Referência ou requisito |
|---|---|
| Controle | Arduino Uno R3, ATmega328P, lógica de 5 V |
| Sensores | 3 × DFRobot SEN0485, 5 V, consumo individual inferior a 5 mA, saída ativa em LOW |
| Relé | DFRobot DFR0017, comando ativo em HIGH, contatos COM e NO |
| Válvula de referência | Adafruit 997, normalmente fechada, 12 V CC, aproximadamente 320 mA a 12 V |
| Conversor | Pololu D24V10F5, saída de 5 V, capacidade típica de até 1 A sujeita às condições térmicas |
| Fonte | Isolada, saída regulada de 12 V / 1 A, com limitação de corrente e proteção contra curto |
| Diodo D1 | 1N4001 em paralelo com a válvula, cátodo no positivo após NO |
| Resistor R1 | 10 kΩ, 1/4 W, de D7 para GND |
| F1 | Referência inicial T750 mA, certificado para CC e com capacidade de interrupção adequada à fonte |

A válvula 997 exige pressão diferencial mínima de 0,02 MPa, aproximadamente 3 psi, e escoamento em um único sentido. Ela pressupõe entrada pressurizada; não é uma seleção para alimentação por gravidade com baixa altura. A vazão de 3 a 12 L/min deve ser estabelecida pela hidráulica da entrada e verificada na montagem. Escolher essa válvula não comprova essa faixa nem o atraso de fechamento de 0,3 s adotado no modelo.

## Balanço de corrente

| Carga em 5 V | Corrente usada no cálculo | Natureza do valor |
|---|---:|---|
| Uno sem periféricos adicionais | 100 mA | Reserva de projeto, não corrente medida |
| Três sensores | 15 mA | Limite superior arredondado dos dados do fabricante |
| Módulo relé energizado | 100 mA | Reserva de projeto a confirmar para a revisão adquirida |
| Total | 215 mA | Soma das parcelas |

Potência de saída do conversor: `5 × 0,215 = 1,075 W`.

Adotando eficiência de cálculo de 80%, a entrada do conversor exige aproximadamente `1,075 / (12 × 0,80) = 0,112 A`. A eficiência é uma hipótese coerente com a faixa típica divulgada, não uma medição nesta carga. Incluindo 1 mA de reserva para consumo próprio, o ramo fica em 0,113 A.

Com a válvula energizada, a fonte fornece aproximadamente `0,320 + 0,113 = 0,433 A`, ou 5,20 W. Com reserva de 25%, são 0,541 A. A fonte de 12 V / 1 A atende a esse orçamento nominal. O conversor de 5 V / 1 A também cobre a reserva de 25% sobre os 215 mA, que resulta em 269 mA. Essas contas não substituem a conferência de temperatura, tolerâncias e transientes.

## Condutores e proteção

Use cobre flexível de 0,50 mm² no circuito de alimentação de 12 V e no ramo da válvula, com até 1 m entre fonte e carga. Para a distribuição de 5 V e sinais, adote 0,20 mm² e até 0,5 m por trecho. Cabos, conectores e isolamento devem admitir a tensão, a corrente e as condições de instalação.

Com resistividade de referência de `0,0175 Ω·mm²/m`, o circuito de ida e volta de 12 V tem `R = 2 × 1 × 0,0175 / 0,50 = 0,070 Ω`. A queda calculada a 0,433 A é 0,030 V. No circuito de 5 V, com ida e volta de 0,5 m e 0,215 A, a queda é aproximadamente 0,019 V. Contatos, conectores e aumento de resistência por temperatura não estão incluídos. As seções foram escolhidas para trechos curtos de bancada; não constituem uma declaração de capacidade de corrente para qualquer instalação.

F1 fica imediatamente após o positivo da fonte, antes da divisão dos ramos. T750 mA é a escolha inicial por estar acima dos 541 mA de orçamento com margem. A confirmação exige a curva tempo-corrente, a corrente de partida e o comportamento da fonte em curto. Uma fonte limitada em corrente pode não fornecer energia suficiente para abrir rapidamente esse fusível. Não se declara coordenação de proteção nem seletividade sem essa análise. A limitação de corrente da fonte continua necessária.

O resistor R1 conduz 0,5 mA quando D7 está em HIGH e dissipa 2,5 mW. O pino D7 comanda somente a entrada do módulo; não fornece a corrente da bobina do relé ou da válvula. O retorno da válvula deve chegar ao negativo da fonte por seu próprio condutor, evitando que a corrente de potência percorra as conexões de sinal do Arduino.

O diodo deve ficar próximo aos terminais da válvula. A Adafruit indica 1N4001 para essa referência. A supressão por diodo pode prolongar a desenergização; por isso, o fechamento hidráulico em 0,3 s permanece uma hipótese de simulação a medir com o diodo instalado. A capacidade de comutação do relé deve ser conferida para carga indutiva CC e para a revisão real do módulo, sem equipará-la à corrente nominal resistiva dos contatos.

## Alimentação do Uno

O conversor alimenta o Uno por um cabo USB de alimentação apropriado. Sensores e módulo relé recebem 5 V em paralelo diretamente da distribuição do conversor. Desconecte a alimentação USB do conversor antes de conectar a USB do computador. Não conecte as duas fontes simultaneamente. Não aplique 12 V aos sinais ou à linha de 5 V.

Este documento fixa a configuração de referência. As indicações genéricas de dimensionamento no desenho devem ser lidas junto com os valores e condições desta memória. O circuito de emergência continua compartilhando Arduino e relé com o controle; não é uma cadeia independente de segurança.

## Fontes

- [DFRobot SEN0485](https://wiki.dfrobot.com/sen0485): alimentação, consumo e sinal.
- [DFRobot DFR0017](https://wiki.dfrobot.com/dfr0017/): módulo e contatos.
- [Adafruit 997](https://www.adafruit.com/product/997): válvula, corrente, pressão mínima e diodo indicado.
- [Pololu D24V10F5](https://www.pololu.com/product/2831): tensão, corrente, eficiência típica e limites térmicos.

As reservas de consumo, as seções dos fios e F1 são decisões de projeto explicitadas neste texto, não valores certificados pelos fabricantes do conjunto.
