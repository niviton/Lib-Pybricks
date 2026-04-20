"""R1 - Comunicacao basica (Hub 2 recebe)"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.led.cor(Color.CYAN)

recebidos = 0
while recebidos < 10:
    msg = robo.receber_ble()
    if not msg:
        wait(50)
        continue

    if len(msg) >= 2 and msg[0] == "contador":
        print("Recebi:", msg)
        robo.atuador.som.beep(frequencia=1000, duracao=80)
        recebidos += 1

robo.atuador.led.cor(Color.GREEN)
