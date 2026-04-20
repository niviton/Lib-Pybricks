"""EXEMPLO 2: Motores por Porta (API nova)"""

from pybricks.parameters import Port
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.atuador.motor.girar(Port.A, sentido="horario", rotacoes=1, potencia=70)
wait(400)
robo.atuador.motor.girar("B1", sentido="anti_horario", rotacoes=0.5, potencia=70)
wait(400)

robo.atuador.motor.arrancar(Port.A, sentido="horario", potencia=60)
wait(1200)
robo.atuador.motor.parar(Port.A)

robo.atuador.motor.ir_posicao(Port.B, posicao=0, sentido="curto", potencia=70)
wait(300)

print("Posicao B:", robo.atuador.motor.posicao(Port.B))
print("Velocidade B:", robo.atuador.motor.velocidade(Port.B))
print("✓ Exemplo 2 finalizado")
