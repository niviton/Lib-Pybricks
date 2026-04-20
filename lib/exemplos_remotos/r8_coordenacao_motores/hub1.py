"""R8 - Coordenacao de 2 motores remotos por porta"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.led.cor(Color.YELLOW)

robo.hub_configurar_portas([
    ("A2", "motor"),
    ("B2", "motor"),
])

robo.atuador.movimento.configurar(esq="A2", dir="B2", cm_por_rotacao=17.5)
robo.atuador.movimento.mover(sentido="frente", cm=20, potencia=75)
wait(600)
robo.atuador.movimento.girar(sentido="direita", graus=90, potencia=75)
wait(600)
robo.atuador.movimento.arrancar(sentido="tras", potencia=65)
wait(900)
robo.atuador.movimento.parar()

robo.atuador.led.cor(Color.GREEN)
