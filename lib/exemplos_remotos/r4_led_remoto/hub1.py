"""R4 - Hub 1 envia cores para LED remoto"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.led.cor(Color.YELLOW)

for cor in (Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLUE, Color.PURPLE, Color.WHITE):
    robo.enviar_ble("cor", cor)
    robo.atuador.som.beep(frequencia=900, duracao=90)
    wait(500)

robo.atuador.led.cor(Color.GREEN)
