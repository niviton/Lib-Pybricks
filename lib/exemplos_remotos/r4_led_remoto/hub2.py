"""R4 - Hub 2 recebe e aplica cor no LED"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

for _ in range(8):
    msg = robo.receber_ble()
    if not msg or len(msg) < 2:
        wait(50)
        continue

    if msg[0] == "cor":
        robo.atuador.led.cor(msg[1])
        robo.atuador.som.beep(frequencia=1200, duracao=90)

robo.atuador.led.cor(Color.GREEN)
