"""R5 - Hub 2 reage a botao remoto"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.led.cor(Color.CYAN)

eventos = 0
while eventos < 15:
    msg = robo.receber_ble()
    if not msg or len(msg) < 2:
        wait(50)
        continue

    if msg[0] == "botao_pressionado":
        eventos += 1
        robo.atuador.led.cor(Color.ORANGE)
        robo.atuador.som.beep(frequencia=1200, duracao=120)
        wait(180)
        robo.atuador.led.cor(Color.CYAN)

robo.atuador.led.cor(Color.GREEN)
