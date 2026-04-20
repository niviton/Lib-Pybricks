"""EXEMPLO 6: Seguidor de linha (API nova por porta)"""

from pybricks.parameters import Port, Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.movimento.configurar(esq=Port.A, dir=Port.B, cm_por_rotacao=17.5)

print("Pressione o botao para iniciar")
robo.esperar_botao()

for _ in range(300):
    e = robo.sensor.cor.reflexao(Port.C)
    d = robo.sensor.cor.reflexao(Port.D)

    if e < 50 and d < 50:
        robo.atuador.movimento.arrancar(sentido="frente", potencia=70)
    elif e < 50:
        robo.atuador.motor.arrancar(Port.A, sentido="horario", potencia=70)
        robo.atuador.motor.arrancar(Port.B, sentido="horario", potencia=40)
    elif d < 50:
        robo.atuador.motor.arrancar(Port.A, sentido="horario", potencia=40)
        robo.atuador.motor.arrancar(Port.B, sentido="horario", potencia=70)
    else:
        robo.atuador.movimento.parar()

    wait(40)

robo.atuador.movimento.parar()
robo.atuador.led.cor(Color.RED)
print("✓ Exemplo 6 finalizado")
