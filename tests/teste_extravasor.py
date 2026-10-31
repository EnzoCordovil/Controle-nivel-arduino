"""Teste preliminar de tubo vertical aberto; nao valida a instalacao real."""
import math
D=.05
G=9.81
SOLEIRA=.0028
CAPACIDADE_ASSUMIDA=.005
Q_CONDUCAO_ASSUMIDO=18/60000

# Conferencia indicativa do tubo de conducao, meio cheio, reto e uniforme.
# Manning n e declividade sao hipoteses, nao caracteristicas medidas.
n=.015;s=.01
area_meia=math.pi*D**2/8
raio_hidraulico=D/4
q_manning=area_meia*raio_hidraulico**(2/3)*s**.5/n
assert q_manning>Q_CONDUCAO_ASSUMIDO
print(f'Conducao indicativa, meio cheio: {q_manning*60000:.2f} L/min; teto adotado no modelo: 18 L/min')

casos=0;maior=0
for area in [.345*.246,.005/.114]:
 for cd in [.2,.3,.4,.5,.6]:
  # Comprimento de crista: perimetro do tubo vertical aberto.
  k=(2/3)*cd*math.pi*D*math.sqrt(2*G)
  for vazao in range(3,13):
   q=vazao/60000
   assert q<Q_CONDUCAO_ASSUMIDO
   h=(q/k)**(2/3)
   v=SOLEIRA+area*h
   assert v<CAPACIDADE_ASSUMIDA
   maior=max(maior,v*1000);casos+=1
  print(f'Area={area*1e4:.2f} cm2, Cd={cd:.1f}, equilibrio a 12 L/min={v*1000:.3f} L')
print(f'PASS: {casos} combinacoes hidraulicas idealizadas; maior volume de equilibrio={maior:.3f} L')
print('Premissas: 5 L ate borda, tubo 50 mm INTERNOS, crista livre e ventilada, descarga nao afogada, conducao >=18 L/min.')
print('Coeficientes a baixa carga sao incertos. As perdas locais, obstrucao, encaixe e dimensoes reais nao foram validados.')
