# Registro de verificação de engenharia

[English](en/ENGINEERING_VERIFICATION.md) | [Português](VERIFICACAO_ENGENHARIA.md)

Ensaios executados em 31/10/2026 sobre o código do commit `21d1c8ae3aee26a1c4d2b93eeb8f891d9f8d3a54`. O firmware foi preservado.

SHA-256 de `ControleNivel/ControleNivel.ino`:

```text
500e459899a0b11b4aed3d9126d9acf1d363b688209859ccfe0785e8e7f47400
```

## Método e resultados

O sketch foi compilado para execução no computador com substitutos das funções do Arduino e da EEPROM. Foram usados g++ 13.3.0, C++11, avisos tratados como erro e detecção de comportamento indefinido. Os modelos hidráulicos em Python foram executados com Python 3.12.14.

| Verificação | Resultado observado |
|---|---|
| Estados, timeouts, ruído, rearme e EEPROM simulada | Asserções concluídas sem falha |
| Partida e passagem de millis por zero | Asserções concluídas sem falha |
| Modelo dinâmico do tanque | 18 cenários explícitos e 210 combinações concluídos conforme as asserções |
| Dez ciclos completos | Corte máximo de aproximadamente 2,030 L a 6 L/min |
| Falha do superior a 12 L/min | Emergência e bloqueio; máximo aproximado de 2,560 L |
| Válvula travada aberta a 12 L/min, extravasor disponível | Equilíbrio aproximado de 3,063 L |
| Geometria atual, sensibilidade hidráulica | 50 combinações; maior equilíbrio aproximado de 3,217 L |
| Geometrias históricas, análise separada | 100 combinações; maior equilíbrio aproximado de 4,216 L |

As 100 combinações históricas não são resultados da geometria atual. Os 18 cenários incluem casos que demonstram limitações: inferior preso indicando água não gera diagnóstico, e válvula travada com extravasor obstruído ultrapassa o limite. Uma asserção aprovada nesses casos significa que a limitação foi reproduzida, não que a falha foi resolvida.

O volume de 6 L registrado no último cenário é uma extrapolação do balanço de volume após ultrapassar a capacidade geométrica; o modelo não representa o derramamento pela borda. A conclusão útil é a ultrapassagem, não o armazenamento físico de 6 L nesse tanque.

## Reprodução e evidência

```bash
bash tests/run_checks.sh
```

O comando salva a saída em `build/evidence/simulation.txt`. Uma cópia da execução desta revisão está em [evidencias/simulacao.txt](evidencias/simulacao.txt). O arquivo identifica o código por hash e registra o ambiente.

A rotina preparada em `.github/workflows/verify.yml` instala Arduino CLI 1.2.2 e Arduino AVR Boards 1.8.6 e executa:

```bash
arduino-cli compile --fqbn arduino:avr:uno --warnings all --output-dir build/uno ControleNivel
```

Também foi configurado o armazenamento dos logs, hashes e binários como artefato `engineering-evidence`. A rotina só comprova compilação depois de uma execução concluída com sucesso. Nesta revisão ela foi preparada, mas não executada: a atualização da branch principal foi bloqueada pela revisão automática de autorização. O ambiente local não dispõe do compilador AVR; a tentativa de obter Arduino CLI não disponibilizou o executável.

## Alcance das conclusões

Os resultados sustentam o comportamento do software e dos modelos nas condições declaradas. Não medem sensores, fonte, fechamento da válvula, vazamentos ou descarga de uma montagem. A compilação AVR verifica compatibilidade e geração do firmware; também não equivale a um ensaio físico. Resultados computacionais devem ser identificados como verificação por simulação ao serem usados no trabalho ou no portfólio.

O [dimensionamento elétrico](DIMENSIONAMENTO_ELETRICO.md) completa a configuração de referência, com corrente, fonte, conversor, condutores e proteção. Reservas de cálculo e verificações de seleção estão explicitadas para permitir reprodução e revisão técnica.
