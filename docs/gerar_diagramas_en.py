"""Render English labels using the same geometry and wiring as the Portuguese sheets."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LABELS = {
    'CONTROLE DE NÍVEL DE ÁGUA': 'WATER LEVEL CONTROL',
    'VISTA ISOMÉTRICA  /  CONJUNTO HIDRÁULICO': 'ISOMETRIC VIEW  /  TANK ASSEMBLY',
    'IDENTIFICAÇÃO DO CONJUNTO': 'ASSEMBLY COMPONENTS',
    'Reservatório transparente': 'Transparent tank',
    'Dimensões internas: 200 × 125 × 230 mm': 'Internal dimensions: 200 × 125 × 230 mm',
    'S1 · início da reposição': 'S1 · start refilling',
    '1,0 L · altura calculada: 44,0 mm': '1.0 L · calculated height: 44.0 mm',
    'S2 · corte normal': 'S2 · normal cutoff',
    '2,0 L · altura calculada: 88,1 mm': '2.0 L · calculated height: 88.1 mm',
    'S3 · emergência': 'S3 · emergency shutdown',
    '2,5 L · altura calculada: 110,1 mm': '2.5 L · calculated height: 110.1 mm',
    'Válvula solenoide de entrada': 'Inlet solenoid valve',
    '12 V CC · normalmente fechada': '12 V DC · normally closed',
    'Dreno com registro manual': 'Manual drain valve',
    'Independente do extravasor': 'Separate from the overflow',
    'Extravasor vertical aberto': 'Open overflow standpipe',
    '2,8 L · crista: 123,3 mm · Ø int.: 50 mm': '2.8 L · rim: 123.3 mm · ID: 50 mm',
    'Descarga por gravidade': 'Gravity discharge',
    'Saída livre, visível e abaixo do tanque': 'Free, visible outlet below the tank',
    'GEOMETRIA DE EXEMPLO — DIMENSÕES INTERNAS ADOTADAS': 'EXAMPLE GEOMETRY: SELECTED INTERNAL DIMENSIONS',
    'Alturas a partir do fundo interno; modelo com tubo de Ø externo 54 mm e Ø interno 50 mm.': 'Heights above the internal floor; pipe model: 54 mm OD and 50 mm ID.',
    'Exemplo calculado, sem vínculo com um recipiente comercial. ~5,47 L até a borda, sem descontar flanges.': 'Calculated example, not a commercial tank specification. About 5.47 L to the rim, excluding flanges.',
    'PRANCHA 01  /  REVISÃO A': 'SHEET 01  /  REVISION A',
    'Enzo Castro Cordovil · 31/10/2026': 'Enzo Castro Cordovil · 31 Oct 2026',
    'DIAGRAMA DE CONEXÕES ELÉTRICAS': 'ELECTRICAL CONNECTION DIAGRAM',
    'Arduino Uno R3  ·  3 × SEN0485  ·  relé DFR0017  ·  válvula 12 V CC': 'Arduino Uno R3  ·  3 × SEN0485  ·  DFR0017 relay  ·  12 V DC valve',
    '01  ALIMENTAÇÃO E CIRCUITO DA VÁLVULA': '01  POWER SUPPLY AND VALVE CIRCUIT',
    'FONTE ISOLADA': 'ISOLATED SUPPLY',
    '12 V CC · corrente a confirmar': '12 V DC · size for load current',
    'Dimensionar para a carga': 'Size for the load',
    'CONVERSOR DC–DC': 'DC-DC CONVERTER',
    '12 V → 5 V regulados': '12 V → regulated 5 V',
    '+5V → USB do Uno': '+5V → Uno USB',
    '+5V → sensores / relé': '+5V → sensors / relay',
    'GND comum em todo o controle': 'Common GND for all control circuits',
    'K1 · contatos do relé': 'K1 · relay contacts',
    'NC: sem ligação': 'NC: unconnected',
    'Válvula 12 V CC · normalmente fechada': '12 V DC valve · normally closed',
    'D1 em paralelo com a bobina': 'D1 across the valve coil',
    'K · faixa': 'K · band',
    '02  SENSORES, COMANDO E REARME': '02  SENSORS, CONTROL AND RESET',
    'D13 · LED integrado': 'D13 · built-in LED',
    'Bloqueio de falha': 'Fault lockout',
    'USB: alimentação 5 V': 'USB: 5 V power input',
    '1,0 L': '1.0 L',
    '2,0 L': '2.0 L',
    '2,5 L': '2.5 L',
    'B1 · rearme momentâneo NA': 'B1 · momentary reset, NO',
    'D4 usa INPUT_PULLUP': 'D4 uses INPUT_PULLUP',
    'Relé ativo em HIGH': 'Active-HIGH relay',
    'COM / NO no circuito 01': 'COM / NO shown in circuit 01',
    'Redes com o mesmo nome estão conectadas. GND = negativo da fonte, buck, Uno, sensores e relé.': 'Matching net labels are connected. GND = common negative for the supply, buck, Uno, sensors and relay.',
    'Alimente o Uno pela USB do conversor; desconecte esse cabo antes de conectar a USB do computador. Não aplicar 12 V em 5V ou sinais.': 'Power the Uno from converter USB; disconnect it before connecting PC USB. Never apply 12 V to 5V or signal pins.',
}


class TranslateLabels(ast.NodeTransformer):
    def visit_Constant(self, node):
        if isinstance(node.value, str) and node.value in LABELS:
            return ast.copy_location(ast.Constant(LABELS[node.value]), node)
        return node


if __name__ == '__main__':
    source = ROOT / 'gerar_diagramas.py'
    tree = TranslateLabels().visit(ast.parse(source.read_text()))
    ast.fix_missing_locations(tree)
    namespace = {'__file__': str(source), '__name__': 'english_diagram_export'}
    exec(compile(tree, str(source), 'exec'), namespace)
    output = ROOT / 'en'
    output.mkdir(exist_ok=True)
    namespace['OUT'] = output
    namespace['cad']()
    namespace['eletrica']()
    print('English PNG and SVG drawings generated in', output)
