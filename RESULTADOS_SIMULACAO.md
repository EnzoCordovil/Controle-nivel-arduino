# Resultados da simulação: tanque de 200 × 125 × 230 mm

[English](docs/en/SIMULATION_RESULTS.md) | [Português](RESULTADOS_SIMULACAO.md)

O modelo usa as dimensões de exemplo de 200 × 125 × 230 mm. O código do Arduino conserva os pinos, os volumes de referência e os prazos de 35 segundos. Em `tests/physical.cpp`, a área interna acima da borda do extravasor é de 0,025 m². O cálculo das alturas considera um tubo com 50 mm de diâmetro interno e 54 mm de diâmetro externo, conforme a [memória de cálculo](docs/GEOMETRIA_E_CONEXOES.md).

## Ensaios de 31/10/2026

Os testes foram compilados em C++11 com `-Wall -Wextra -Werror -fsanitize=undefined`. O modelo dinâmico também usou `-O1`. Os executáveis e os dois testes Python terminaram com código zero. Esta execução não incluiu compilação AVR nem ensaios na montagem física.

| Verificação | Resultado |
|---|---|
| Lógica, partida, filtros, prazos, EEPROM simulada, rearme e retorno de millis | Passou nas verificações implementadas |
| 18 cenários dinâmicos, incluindo dez ciclos | Resultados esperados |
| 210 combinações normais de vazão e volume inicial | Sem bloqueios indevidos nas premissas |
| Normal a 6 L/min | Máximo de 2,030 L |
| Emergência com falha do superior e entrada de 12 L/min | Máximo de 2,560 L |
| Superior e emergência falham indicando seco; extravasor funcional | Máximo de 3,063 L |
| Válvula travada aberta a 12 L/min; extravasor funcional | Equilíbrio de aproximadamente 3,063 L |
| 50 combinações hidráulicas da geometria de exemplo | Maior equilíbrio de 3,217 L, com Cd=0,2 |
| Teste das duas geometrias históricas | 100 combinações; maior equilíbrio de 4,216 L |
| Válvula travada e extravasor obstruído | Modelo ultrapassa 5 L; limitação conhecida |
| Inferior preso indicando água | Falta de reposição sem diagnóstico; limitação conhecida |

Os valores de 3,692 L e 4,216 L no registro histórico pertencem às geometrias anteriores. Esses testes foram mantidos para comparação. No exemplo atual, o volume calculado até a borda é de 5,468 L, sem descontar flanges, e o limite de cálculo permanece em 5 L.

O modelo adota coeficientes Cd, capacidade de condução de pelo menos 18 L/min, descarga sem afogamento e atraso de fechamento de 300 ms. Esses parâmetros são hipóteses de cálculo, sem medição na montagem.

---

## Registro histórico das geometrias anteriores

## Procedimento

A versão de 35 s foi testada antes de atualizar os arquivos. O teste do novo prazo falhou com o código anterior de 65 s e passou após a alteração. O arquivo .ino foi executado em C++11, com funções Arduino e EEPROM simuladas, -Wall -Wextra -Werror e UndefinedBehaviorSanitizer. Essa execução também não incluiu compilação AVR ou ensaio físico.

Os testes abrangeram a lógica do programa, 18 cenários dinâmicos, 210 combinações de vazão e volume inicial, dez ciclos completos e 100 combinações hidráulicas. Cada caso apresentou o resultado esperado. Nos testes de limites, esse resultado é a reprodução de uma falha conhecida, como o transbordamento com válvula travada e extravasor obstruído.

## Alterações consolidadas após os testes

- Inferior 1 L; superior 2 L; emergência 2,5 L.
- Dois prazos de supervisão de 35 s (1 L / 2 L/min = 30 s, mais 5 s).
- Extravasor: tubo vertical aberto, referência de 50 mm internos e crista em 2,8 L; substitui abertura circular alta na parede.
- Mantidos pinos D2/D3/D5, relé D7, botão D4 e persistência de bloqueio.

## Modelo e hipóteses

Passo de 1 ms, sensores ideais nas referências volumétricas e fechamento da válvula com atraso assumido de 300 ms. Ganho líquido mínimo de cálculo: 2 L/min; entrada entre 3 e 12 L/min. O recipiente é idealizado com 5 L na borda, o que não foi comprovado pelo produto comercial.

Extravasão por modelo de crista circular horizontal: Q = (2/3) Cd pi D sqrt(2g) H^(3/2), limitada à capacidade de condução assumida de 18 L/min. Cd=0,4 no ensaio dinâmico; sensibilidade entre 0,2 e 0,6. A área horizontal do tanque no ensaio dinâmico usa a pegada externa de 848,7 cm² como cenário; outra área equivalente de 438,6 cm² foi examinada na sensibilidade. São modelos de cálculo, não levantamento geométrico. Na montagem, calibrar volumes com o tubo instalado para incluir o deslocamento.

Como conferência de ordem de grandeza, Manning para trecho reto de 50 mm internos, meio cheio, n=0,015 e declividade de 1% dá cerca de 21,15 L/min. O teto de 18 L/min não foi demonstrado para o percurso concreto; curvas, passagem de fundo, ventilação, afogamento e obstruções exigem avaliação. Não se utiliza sifão no modelo. Não foram modeladas tensões mecânicas da parede ou o encaixe de conexões no recipiente.

Bases conceituais públicas: [equação de vertedores, USACE HEC-HMS](https://www.hec.usace.army.mil/confluence/hmsdocs/hmstrm/reservoir-modeling/reservoir-modeling-concepts-and-equations/spillways) e [seleção de vertedores e efeitos de pequena carga, USBR](https://www.usbr.gov/tsc/techreferences/mands/wmm/chap07_16.html). A aplicação em pequena escala é uma aproximação com coeficientes assumidos, não uma calibração fornecida por essas fontes.

## Resultados principais

| Ensaio | Resultado no modelo |
|---|---|
| Normal, 6 L/min | Corte normal com máximo de 2,030 L |
| Normal, 3 L/min | Máximo de 2,015 L, sem bloqueio indevido |
| Entrada 3 e retirada 1 L/min | Máximo de 2,010 L, sem bloqueio |
| Entrada 6 e retirada 1 L/min por 10 min | Máximo de 2,025 L, sem bloqueio |
| Superior falha seco, 12 L/min | Emergência bloqueia, máximo de 2,560 L |
| Inferior e superior secos, emergência funcional | Emergência bloqueia, máximo de 2,560 L |
| Superior e emergência secos, 12 L/min, extravasor funcional | Máximo de 3,692 L; bloqueia por tempo e depois escoa |
| Válvula travada aberta a 12 L/min, extravasor funcional | Equilíbrio em ~3,692 L, comando desligado e bloqueado |
| Dez ciclos completos | Máximo de 2,030 L |
| 210 combinações normais (3–12 L/min; início de 0–2 L) | Sem bloqueio indevido, máximos abaixo de 2,07 L |
| Sensibilidade hidráulica: 100 combinações | Maior equilíbrio calculado: 4,216 L, com Cd=0,2 |
| Religamento após falha gravada e rearme manual | Comportamento esperado |
| Oscilações, botão preso, retorno de millis a zero | Comportamento esperado |

## Limites reproduzidos

- Inferior preso indicando água: tanque vazio permanece sem reposição e sem alarme; não é possível identificá-lo inequivocamente só com os sensores altos.
- Válvula travada e extravasor obstruído: ultrapassa cinco litros. Software não resolve essa combinação.
- Valores de equilíbrio são condicionais às hipóteses hidráulicas. Alterar a condução, geometria, volume real até a borda ou coeficientes pode mudar o resultado.
- EEPROM simulada grava instantaneamente; não comprova tolerância a perda de energia durante uma gravação.

## Conclusão

A versão passou nos cenários de operação e de proteção previstos, dentro das premissas do modelo. Texto e código foram atualizados somente depois desses resultados. Isso não equivale a funcionamento universal ou aprovação física do sistema: instalação, capacidade de escoamento, vedação, dimensões reais e alimentação precisam ser verificadas na montagem.

## Verificação posterior para Arduino Uno

A [execução no GitHub Actions](https://github.com/EnzoCastro-neko/controle-nivel-agua-arduino/actions/runs/41200581064) compilou o mesmo firmware para `arduino:avr:uno` com sucesso e repetiu as simulações. Foram usados Arduino CLI 1.2.2 e Arduino AVR Boards 1.8.6. Consulte o [registro de engenharia](docs/VERIFICACAO_ENGENHARIA.md) para memória utilizada, avisos do core e logs. Os relatos anteriores de ausência de compilação AVR descrevem as execuções históricas, anteriores a esta verificação. Ensaios físicos continuam fora do escopo dos resultados computacionais.
