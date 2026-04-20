"""R7 - Hub 1 agrega sensores remotos por porta"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.led.cor(Color.YELLOW)

robo.sensor.cor.configurar("A2")
robo.sensor.distancia.configurar("C2")

for _ in range(40):
    r = robo.sensor.cor.reflexao("A2")
    d = robo.sensor.distancia.ler("C2")
    print("A2:", r, "| C2:", d)
    wait(100)

robo.atuador.led.cor(Color.GREEN)
