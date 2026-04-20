"""R0 - API nova completa (Hub 1)"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.led.cor(Color.YELLOW)

robo.hub_configurar_portas([
    ("A2", "motor"),
    ("B2", "motor"),
    ("C2", "sensor_ultra"),
    ("D2", "sensor_cor", "reflexao"),
])

robo.atuador.movimento.configurar(esq="A2", dir="B2", cm_por_rotacao=17.5)

for _ in range(40):
    if robo.hub.botao.pressionado():
        robo.atuador.som.beep(frequencia=1200, duracao=80)

    dist = robo.sensor.distancia.ler("C2")
    ref = robo.sensor.cor.reflexao("D2")

    if dist < 180:
        robo.atuador.movimento.parar()
        robo.atuador.led.cor(Color.RED)
    elif ref > 30:
        robo.atuador.movimento.arrancar(sentido="frente", potencia=70)
        robo.atuador.led.cor(Color.GREEN)
    else:
        robo.atuador.movimento.girar(sentido="esquerda", graus=20, potencia=65)
        robo.atuador.led.cor(Color.ORANGE)

    wait(80)

robo.atuador.movimento.parar()
robo.atuador.motor.girar("A2", sentido="horario", rotacoes=0.5, potencia=80)
robo.atuador.motor.girar("B2", sentido="anti_horario", rotacoes=0.5, potencia=80)
robo.atuador.led.cor(Color.GREEN)
