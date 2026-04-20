"""R9 - Transmissao de dados com ACK (Hub 2)"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.led.cor(Color.CYAN)

for i in range(4):
    msg = robo.receber_ble()
    if not msg:
        wait(50)
        continue

    print("Recebido:", msg)
    robo.enviar_ble("ack", i)
    robo.atuador.som.beep(frequencia=1000, duracao=80)
    robo.atuador.led.cor(Color.GREEN)
    wait(200)
    robo.atuador.led.cor(Color.CYAN)

robo.atuador.led.cor(Color.GREEN)
