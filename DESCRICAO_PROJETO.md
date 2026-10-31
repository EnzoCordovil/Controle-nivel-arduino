# Projeto de Controle Automático de Nível de Água

O projeto controla o enchimento de um reservatório plástico transparente, com capacidade nominal de cinco litros e dimensões gerais de referência de 34,5 × 24,6 × 11,4 cm. A água vem de uma torneira, passa por uma válvula solenoide de 12 V CC normalmente fechada e entra por uma conexão fixa na lateral próxima à base.

Três sensores capacitivos externos informam o nível ao Arduino Uno. O controle inicia a reposição quando a água baixa do sensor de referência de 1 litro e encerra quando alcança o sensor de 2 litros. Um terceiro sensor, na referência de 2,5 litros, provoca fechamento e bloqueio de emergência. As alturas de instalação são estabelecidas pelos volumes medidos, com todos os componentes hidráulicos internos já instalados.

A alimentação utiliza uma fonte externa isolada e regulada de 12 V / 1 A. Um conversor fornece 5 V para o Arduino, o módulo relé e os sensores. A válvula recebe 12 V pelos contatos comum e normalmente aberto do relé; um diodo 1N4001 protege contra o pico de tensão da bobina. O comando usa resistor de 10 kΩ para manter o relé desligado durante a inicialização.

O programa verifica os sinais antes de permitir o enchimento e prevê dois prazos de supervisão de 35 segundos: da abertura à detecção do sensor inferior e dessa detecção à do sensor superior. Cada etapa acrescenta aproximadamente um litro. Com ganho líquido de água de 2 L/min, o tempo calculado é de 30 segundos, acrescido de cinco segundos de margem. O corte por nível tem prioridade sobre os prazos.

Excesso de tempo, sinais incompatíveis ou acionamento da emergência bloqueiam o sistema. O bloqueio permanece registrado na EEPROM após desligamento e exige o botão de rearme. A liberação depende de nova verificação dos sensores e não força a abertura da válvula.

O extravasor adota um tubo vertical aberto dentro do reservatório, com diâmetro interno de referência de 50 mm e borda superior no volume de referência de 2,8 litros. A água excedente entra pela borda do tubo e segue por uma passagem estanque no fundo, sobre base com espaço para a conexão, até uma tubulação de descarte livre e visível, sem registro. O reservatório e o percurso permanecem ventilados; o projeto não depende de sifonamento. A condução prevê trecho curto, sem contrapendentes, inclinação mínima de referência de 1% nos trechos horizontais e destino abaixo do tanque, com desnível de até um metro. Conexões e base devem sustentar o conjunto sem carregar a parede plástica com o peso dos tubos.

Um dreno manual separado, próximo à base, permite esvaziamento ou transferência. Sua utilização não faz parte do comando eletrônico, mas influencia o ganho líquido de água durante o enchimento.

As simulações de software reproduziram o controle normal e as proteções especificadas. O modelo hidráulico preliminar apresentou equilíbrio abaixo do limite assumido de cinco litros com entrada de até 12 L/min. Esses resultados dependem das hipóteses documentadas no relatório e não representam ensaio físico da montagem, validação da capacidade nominal até a borda ou aprovação de todas as falhas possíveis.
