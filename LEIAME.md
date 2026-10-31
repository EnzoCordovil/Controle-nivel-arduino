# Controle de nível — configuração revisada

Abra ControleNivel/ControleNivel.ino no Arduino IDE e selecione Arduino Uno R3 (ATmega328P). EEPROM acompanha Arduino AVR Boards. Sem bibliotecas externas.

## Configuração vigente

| Função | Volume de referência | Pino |
|---|---:|---|
| Iniciar reposição | 1 L | D2 |
| Encerrar reposição | 2 L | D3 |
| Emergência: fechar e bloquear | 2,5 L | D5 |
| Rearme momentâneo normalmente aberto | — | Entre D4 e GND |
| Comando do relé, ativo em HIGH | — | D7 |
| LED de bloqueio | — | Integrado D13 |
| Borda do tubo extravasor | 2,8 L | Sem comando elétrico |

Sensores SEN0485, ativos em LOW. Posicionar pelos volumes medidos após instalar o tubo interno, pois ele desloca água. Conferir alcance de detecção de 3 mm, espessura, fixação e interferências. Não converter diretamente litros em centímetros a partir das dimensões externas.

Fonte externa isolada de 12 V / 1 A. Conversor fornece 5 V regulados, capacidade especificada de 1 A. Arduino pela USB; sensores e módulo relé em paralelo na distribuição de 5 V; GND comum do controle. Resistor de 10 kΩ de D7 para GND. Válvula de 12 V pelos contatos COM/NO, NC livre; retorno direto ao negativo da fonte. Diodo 1N4001 em paralelo com a bobina, faixa no positivo após NO. Nunca aplicar 12 V aos pinos de sinal/5 V ou à USB. Desconectar alimentação USB do conversor antes de conectar computador. Fechar proteção contra sobrecorrente e polaridade com a fonte e os fios concretos.

## Programa

- Partida: pelo menos 1 s com relé desligado; aguarda sensores estáveis.
- Inferior seco: inicia enchimento; superior encerra normalmente.
- Entre níveis na partida: aguarda baixar; não força enchimento.
- Primeiro prazo: 35 s até inferior detectar; segundo: 35 s da primeira detecção confirmada do inferior até superior. Sem reiniciar a segunda contagem por oscilação.
- Sinal bruto do superior interrompe comando imediatamente; confirmação de 100 ms encerra ciclo.
- Emergência D5 provoca bloqueio imediato, inclusive na partida; não espera filtro. Ruído pode causar bloqueio: inspecionar antes do rearme.
- Superior molhado e inferior seco: bloqueio por inconsistência confirmada.
- Botão: INPUT_PULLUP e filtro de 40 ms. Exige soltar após falha e depois apertar novamente. Sensores devem estar estáveis/coerentes e emergência inativa.
- Bloqueio usa byte 0 da EEPROM e persiste após RESET ou desligamento. Gravação não é redundante ou tolerante a interrupção de energia durante a escrita.
- Monitor Serial: 9600 baud.

## Prazos e vazões

Os prazos anteriores de 65 s foram substituídos por 35 s. Para cada litro acrescentado com ganho líquido mínimo assumido de 2 L/min: 30 s + 5 s. Entrada de cálculo 3 a 12 L/min. A retirada deve manter ganho líquido de pelo menos 2 L/min para que os prazos sejam compatíveis. Retirada excessiva ou entrada abaixo dessa premissa podem gerar bloqueio por demora sem defeito dos sensores.

## Extravasor revisado

A abertura circular alta na parede foi substituída por um tubo vertical aberto de 50 mm INTERNOS de referência, com crista em 2,8 L. DN comercial não garante esse diâmetro interno. Escoa por passagem estanque no fundo, sobre base preparada com vão, até descarte livre abaixo do tanque. Não usar registro, sifão, mangueira dobrada, saída submersa ou ligação direta fechada ao esgoto. Manter ventilação e saída visível. Trecho curto e descendente; inclinação de referência mínima de 1% nos trechos horizontais, desnível total de até 1 m. Confirmar vedação, compatibilidade e reforço/suporte da passagem no recipiente; não perfurar sem conferir o encaixe real.

Modelo: capacidade de condução assumida de pelo menos 18 L/min e crista livre. Cálculo de Manning para tubo reto de 50 mm internos, meio cheio, n=0,015 e 1% de declividade dá cerca de 21,15 L/min, mas não valida curvas, entrada, trechos verticais ou conexão concreta. O teto de 18 L/min é hipótese de simulação, não capacidade medida. Verificar por ensaio e dimensionamento da montagem real.

## Limitações

Inferior travado indicando água pode impedir reposição sem alarme. Terceiro sensor compartilha Arduino/relé e não é circuito de segurança independente. Válvula travada depende do extravasor; se ele estiver obstruído ou subdimensionado, pode transbordar. Medidas internas, volume até borda, coeficientes de escoamento em baixa carga, fonte/temperatura e atrasos reais não estão fisicamente validados. O tubo interno desloca volume e deve caber com conexões, suporte e sensores.

## Repetir simulação

    g++ -std=c++11 -Wall -Wextra -Werror -Itests tests/test.cpp -o teste_logica
    ./teste_logica
    g++ -std=c++11 -Wall -Wextra -Werror -Itests tests/physical.cpp -o teste_tanque
    ./teste_tanque
    python3 tests/teste_extravasor.py

Leia DESCRICAO_PROJETO.md e RESULTADOS_SIMULACAO.md. Compilação AVR e ensaio físico não foram realizados neste ambiente.
