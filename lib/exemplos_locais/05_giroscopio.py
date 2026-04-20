"""EXEMPLO 5: Giroscopio + Movimento (API nova)"""

from pybricks.parameters import Port
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.sensor.giroscopio.resetar()
print("Angulo inicial:", robo.sensor.giroscopio.angulo())

robo.atuador.movimento.configurar(esq=Port.A, dir=Port.B, cm_por_rotacao=17.5)
robo.atuador.movimento.mover(sentido="frente", cm=15, potencia=70)
wait(400)
robo.atuador.movimento.girar(sentido="direita", graus=90, potencia=70)
wait(300)

print("Angulo final:", robo.sensor.giroscopio.angulo())
print("✓ Exemplo 5 finalizado")
