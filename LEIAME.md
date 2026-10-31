# Montagem e configuração do controle de nível

[English](docs/en/ASSEMBLY.md) | [Português](LEIAME.md)

Abra `ControleNivel/ControleNivel.ino` no Arduino IDE e selecione Arduino Uno R3 (ATmega328P). A biblioteca EEPROM acompanha o pacote Arduino AVR Boards; o código não usa bibliotecas externas.

## Pinos e níveis

| Função | Volume de referência | Pino |
|---|---:|---|
| Iniciar reposição | 1 L | D2 |
| Encerrar reposição | 2 L | D3 |
| Emergência: fechar e bloquear | 2,5 L | D5 |
| Rearme momentâneo normalmente aberto | — | Entre D4 e GND |
| Comando do relé, ativo em HIGH | — | D7 |
| LED de bloqueio | — | Integrado D13 |
| Borda do tubo extravasor | 2,8 L | Sem comando elétrico |

Os sensores SEN0485 enviam LOW quando detectam água. O fio vermelho recebe 5 V, o preto vai ao GND e o verde leva o sinal OUT ao Arduino.

No tanque de exemplo de 200 × 125 × 230 mm internos, com tubo de 54 mm de diâmetro externo, as alturas calculadas dos sensores são 44,0, 88,1 e 110,1 mm. A borda do extravasor fica a 123,3 mm. Essas dimensões foram escolhidas para o exemplo. Na montagem, ajuste as posições pelos volumes medidos com o tubo instalado, pois ele ocupa espaço dentro do tanque.

O sensor tem alcance de detecção de 3 mm. Confira a espessura da parede, a fixação e possíveis interferências. Para calcular as alturas, use a geometria interna do tanque e o espaço ocupado pelas peças.

## Alimentação e relé

A referência de alimentação é uma fonte externa isolada de 12 V / 1 A e um conversor com saída regulada de 5 V / 1 A. O conversor alimenta o Arduino pela USB. Os sensores e o módulo relé recebem 5 V em paralelo, com GND comum ao controle.

Ligue um resistor de 10 kΩ entre D7 e GND. A válvula de 12 V recebe alimentação pelos contatos COM e NO do relé, com retorno ao negativo da fonte. Deixe NC sem conexão. O diodo 1N4001 fica em paralelo com a bobina, com a faixa voltada para o positivo após o contato NO.

Não aplique 12 V aos pinos de sinal, ao pino 5V ou à USB. Antes de conectar o computador, desconecte o cabo USB que vem do conversor. Dimensione a fonte, os condutores e a proteção contra sobrecorrente para a carga escolhida e confira a polaridade antes de energizar.

## Programa

- Ao iniciar, o programa mantém o relé desligado por pelo menos 1 s e aguarda a estabilização dos sensores.
- O enchimento começa com o sensor inferior seco e termina quando o superior detecta água. Se a partida ocorrer entre esses níveis, o programa aguarda a água baixar.
- O primeiro prazo é de 35 s até a detecção do inferior. O segundo começa nessa primeira detecção confirmada e dura até 35 s para alcançar o superior. Oscilações do inferior não reiniciam essa contagem.
- O sinal bruto do superior interrompe o comando imediatamente. Após 100 ms de confirmação, o programa encerra o ciclo.
- A emergência em D5 bloqueia o sistema imediatamente, inclusive durante a partida. Essa entrada não aguarda o filtro; se houver acionamento por ruído, confira a causa antes de rearmar.
- Se o superior indicar água e o inferior permanecer seco, a confirmação dessa combinação provoca bloqueio.
- O botão usa INPUT_PULLUP e filtro de 40 ms. Após uma falha, é preciso soltá-lo e pressioná-lo novamente. O rearme exige sensores estáveis e coerentes, com a emergência inativa.
- O bloqueio ocupa o byte 0 da EEPROM e permanece após RESET ou desligamento. A gravação não tem redundância nem proteção contra interrupção de energia durante a escrita.
- O Monitor Serial usa 9600 baud.

## Prazos e vazões

Cada etapa tem prazo de 35 s. Acrescentar 1 litro com ganho líquido de 2 L/min leva 30 s; os 5 s restantes são a margem adotada. A faixa de entrada usada nos cálculos é de 3 a 12 L/min.

Se houver retirada de água durante o enchimento, o ganho líquido precisa continuar em pelo menos 2 L/min. Abaixo desse valor, o programa pode bloquear por demora mesmo com os sensores funcionando. O prazo anterior de 65 s foi substituído por esse ajuste de 35 s.

## Extravasor

O extravasor é um tubo vertical aberto com diâmetro interno de referência de 50 mm e borda na altura de 2,8 L. Confira o diâmetro interno do produto escolhido: a bitola nominal DN, sozinha, não define essa medida.

A descarga atravessa o fundo por uma conexão estanque e segue até um ponto de descarte abaixo do tanque. A base deve deixar espaço para a conexão. Mantenha o percurso curto e descendente, com inclinação de referência mínima de 1% nos trechos horizontais e desnível total de até 1 m.

A saída precisa ficar livre, visível e ventilada. Evite registro, sifão, mangueira dobrada, saída submersa ou ligação direta fechada ao esgoto. Antes de perfurar, confira o encaixe das peças, a vedação e o suporte da passagem de fundo.

O modelo considera a borda livre e capacidade de condução de pelo menos 18 L/min. Pela equação de Manning, um tubo reto de 50 mm internos, meio cheio, com n=0,015 e declividade de 1%, conduz cerca de 21,15 L/min. Esse cálculo não inclui as perdas em curvas, na entrada ou nas conexões. Os 18 L/min são uma hipótese da simulação; a capacidade da montagem depende do dimensionamento e do ensaio do percurso completo.

## Limitações

Se o sensor inferior travar indicando água, o tanque pode ficar sem reposição e sem alarme. O terceiro sensor compartilha o Arduino e o relé com os demais, portanto não forma um circuito de segurança independente. Se a válvula travar aberta, o escoamento depende do extravasor; uma obstrução ou capacidade insuficiente pode causar transbordamento.

O tubo ocupa parte do volume e precisa caber junto com as conexões, os suportes e os sensores. As dimensões internas, o volume até a borda e os coeficientes de escoamento em baixa carga ainda não foram medidos na montagem. O mesmo vale para os atrasos reais e o comportamento da alimentação com a temperatura.

## Repetir simulação

    g++ -std=c++11 -Wall -Wextra -Werror -Itests tests/test.cpp -o teste_logica
    ./teste_logica
    g++ -std=c++11 -Wall -Wextra -Werror -Itests tests/physical.cpp -o teste_tanque
    ./teste_tanque
    python3 tests/teste_extravasor.py
    python3 tests/teste_geometria_exemplo.py

Leia DESCRICAO_PROJETO.md e RESULTADOS_SIMULACAO.md. Compilação AVR e ensaio físico não foram realizados neste ambiente.

Consulte o [diagrama elétrico e a memória de cálculo](docs/GEOMETRIA_E_CONEXOES.md). Na montagem, confira a identificação dos bornes no módulo escolhido.

## Configuração elétrica de referência

Consulte [DIMENSIONAMENTO_ELETRICO.md](docs/DIMENSIONAMENTO_ELETRICO.md) para a seleção da válvula, fonte, conversor, condutores e F1, com orçamento de corrente e condições de aplicação.
