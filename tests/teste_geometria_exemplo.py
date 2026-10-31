"""Memória de cálculo reproduzível para a geometria de exemplo, não medida."""
import math

COMPRIMENTO = .200
LARGURA = .125
ALTURA = .230
DIAMETRO_INTERNO = .050
DIAMETRO_EXTERNO = .054
AREA = COMPRIMENTO * LARGURA
AREA_TUBO = math.pi * DIAMETRO_EXTERNO ** 2 / 4
AREA_UTIL = AREA - AREA_TUBO
V_CRISTA = .0028
H_CRISTA = V_CRISTA / AREA_UTIL
DESLOCAMENTO = AREA_TUBO * H_CRISTA
CAPACIDADE = AREA * ALTURA - DESLOCAMENTO


def altura(volume):
    if volume <= V_CRISTA:
        return volume / AREA_UTIL
    return H_CRISTA + (volume - V_CRISTA) / AREA


for litros in [1, 2, 2.5, 2.8, 5]:
    h = altura(litros / 1000)
    assert 0 < h < ALTURA
    print(f'{litros:.1f} L -> {h*1000:.3f} mm acima do fundo interno')
assert DIAMETRO_EXTERNO < LARGURA
assert CAPACIDADE > .005
print(f'Volume bruto={AREA*ALTURA*1000:.3f} L; deslocamento do tubo={DESLOCAMENTO*1000:.3f} L')
print(f'Volume líquido geométrico até a borda={CAPACIDADE*1000:.3f} L')

casos = 0
maior = 0
for cd in [.2, .3, .4, .5, .6]:
    k = (2/3) * cd * math.pi * DIAMETRO_INTERNO * math.sqrt(2*9.81)
    for q_l_min in range(3, 13):
        q = q_l_min / 60000
        assert q_l_min < 18  # capacidade de condução ASSUMIDA, não ensaiada
        carga = (q / k) ** (2/3)
        volume = V_CRISTA + AREA * carga
        assert H_CRISTA + carga < ALTURA
        assert volume < .005  # limite de cálculo conservador abaixo da borda
        maior = max(maior, volume)
        casos += 1
    print(f'Cd={cd:.1f}: equilíbrio a 12 L/min={volume*1000:.3f} L')
print(f'PASS: {casos} combinações do exemplo; maior equilíbrio={maior*1000:.3f} L')
print('Modelo ideal: paredes retas; tubo vertical livre; sem flanges no volume; sem afogamento.')
print('Requer verificar rigidez, conexões, espessura da parede, vazão e capacidade real de descarga.')
