"""R6 - Jogo 2 jogadores (Hub 1)"""

from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.esperar_botao()
robo.atuador.led.cor(Color.YELLOW)
robo.atuador.som.beep(frequencia=800, duracao=100)

timer = StopWatch()
contador = 0
while timer.time() < 10000:
    if robo.hub.botao.pressionado():
        contador += 1
        robo.enviar_ble("placar_h1", contador)
        robo.atuador.som.beep(frequencia=1000, duracao=80)
        wait(250)
    wait(20)

robo.atuador.led.cor(Color.GREEN)
print("Pontos H1:", contador)
