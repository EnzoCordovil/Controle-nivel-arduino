# Projeto de controle automático de nível de água

[English](docs/en/PROJECT.md) | [Português](DESCRICAO_PROJETO.md)

O sistema controla o enchimento de um tanque retangular transparente. Para o exemplo, foram escolhidas dimensões internas de 20 × 12,5 × 23 cm. Com o tubo extravasor instalado, o volume calculado até a borda é de aproximadamente 5,47 litros, sem descontar flanges e outras conexões. Os cálculos usam o limite de 5 litros para manter uma margem abaixo da borda.

A água sai de uma torneira, passa por uma válvula solenoide de 12 V CC normalmente fechada e entra no tanque por uma conexão lateral próxima à base.

Três sensores capacitivos, fixados por fora do tanque, enviam os sinais de nível ao Arduino Uno. A reposição começa quando a água baixa do sensor de 1 litro e termina ao atingir o de 2 litros. O terceiro sensor fica na referência de 2,5 litros e aciona o fechamento e o bloqueio de emergência. Na montagem, as posições devem corresponder aos volumes de água com todos os componentes internos instalados.

A alimentação de referência usa uma fonte externa isolada e regulada de 12 V / 1 A. Um conversor fornece 5 V para os sensores, o módulo relé e a alimentação USB do Arduino. A válvula recebe 12 V pelos contatos COM e NO do relé. Um diodo 1N4001, em paralelo com a bobina, limita o pico de tensão no desligamento. O resistor de 10 kΩ entre o comando e o GND mantém o relé desligado durante a inicialização.

O programa verifica os sinais antes de permitir o enchimento e prevê dois prazos de supervisão de 35 segundos: da abertura à detecção do sensor inferior e dessa detecção à do sensor superior. Cada etapa acrescenta aproximadamente um litro. Com ganho líquido de água de 2 L/min, o tempo calculado é de 30 segundos, acrescido de cinco segundos de margem. O corte por nível tem prioridade sobre os prazos.

O sistema bloqueia o enchimento se o tempo for excedido, os sinais dos sensores forem incompatíveis ou a emergência for acionada. A EEPROM guarda esse bloqueio mesmo após desligar a alimentação. O botão de rearme permite uma nova verificação dos sensores; o programa só volta a abrir a válvula quando as condições de enchimento forem atendidas.

O extravasor adota um tubo vertical aberto dentro do reservatório, com diâmetro interno de referência de 50 mm e borda superior no volume de referência de 2,8 litros. A água excedente entra pela borda do tubo e segue por uma passagem estanque no fundo, sobre base com espaço para a conexão, até uma tubulação de descarte livre e visível, sem registro. O reservatório e o percurso permanecem ventilados; o projeto não depende de sifonamento. A condução prevê trecho curto, sem contrapendentes, inclinação mínima de referência de 1% nos trechos horizontais e destino abaixo do tanque, com desnível de até um metro. Conexões e base devem sustentar o conjunto sem carregar a parede plástica com o peso dos tubos.

Um dreno manual separado, próximo à base, permite esvaziamento ou transferência. Sua utilização não faz parte do comando eletrônico, mas influencia o ganho líquido de água durante o enchimento.

As simulações reproduziram os ciclos de enchimento e as proteções descritas no programa. Para entradas de até 12 L/min, o modelo hidráulico calculou o equilíbrio abaixo de 5 litros. O [relatório](RESULTADOS_SIMULACAO.md) registra as hipóteses de escoamento, os resultados e as falhas que o sistema consegue identificar. Os ensaios apresentados são de software e cálculo hidráulico; não incluem medições da montagem.

A [memória de cálculo e ligações](docs/GEOMETRIA_E_CONEXOES.md) reúne a vista 3D, as alturas dos sensores e o esquema elétrico.
