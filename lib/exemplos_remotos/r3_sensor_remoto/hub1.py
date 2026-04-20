"""R3 - Leitura de sensor remoto por porta"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.led.cor(Color.YELLOW)

robo.sensor.cor.configurar("A2")
robo.sensor.distancia.configurar("C2")

for _ in range(30):
    print("Reflexao A2:", robo.sensor.cor.reflexao("A2"), "| Dist C2:", robo.sensor.distancia.ler("C2"))
    wait(150)

robo.atuador.led.cor(Color.GREEN)
