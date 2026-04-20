"""EXEMPLO 3: Sensor de Cor por Porta (API nova)"""

from pybricks.parameters import Port
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

print("Lendo reflexao em D...")
for _ in range(12):
    reflexao = robo.sensor.cor.reflexao(Port.D)
    print("Reflexao D:", reflexao)
    wait(250)

print("Cor lida em D:", robo.sensor.cor.ler(Port.D))
print("Calibracao opcional: aproxime o alvo da cor por 2s")
robo.sensor.cor.calibrar(Port.D, "azul_teste", segundos=2)
print("✓ Exemplo 3 finalizado")
