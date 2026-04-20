"""R1 - Comunicacao basica (Hub 1 envia)"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.led.cor(Color.YELLOW)

for i in range(10):
    robo.enviar_ble("contador", i)
    robo.atuador.som.beep(frequencia=800, duracao=80)
    wait(600)

robo.atuador.led.cor(Color.GREEN)
