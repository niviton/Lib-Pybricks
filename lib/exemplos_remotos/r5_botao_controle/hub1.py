"""R5 - Hub 1 envia evento de botao"""

from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.led.cor(Color.YELLOW)

clock = StopWatch()
contador = 0
while clock.time() < 15000:
    if robo.hub.botao.pressionado():
        contador += 1
        robo.enviar_ble("botao_pressionado", contador)
        robo.atuador.som.beep(frequencia=1000, duracao=120)
        wait(300)
    wait(40)

robo.atuador.led.cor(Color.GREEN)
