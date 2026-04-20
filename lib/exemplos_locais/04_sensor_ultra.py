"""EXEMPLO 4: Distancia por Porta (API nova)"""

from pybricks.parameters import Port
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

for _ in range(20):
    dist_mm = robo.sensor.distancia.ler(Port.C)
    print("Distancia C:", dist_mm, "mm")
    wait(200)

print("✓ Exemplo 4 finalizado")
