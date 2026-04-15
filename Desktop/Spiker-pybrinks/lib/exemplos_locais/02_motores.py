"""EXEMPLO 2: Motores"""

from pybricks.parameters import Port, Direction
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.adicionar_motor_local("motor1", Port.A)
robo.adicionar_motor_local("motor2", Port.B, Direction.COUNTERCLOCKWISE)

# Girar 360 graus
robo.motor_local_graus("motor1", 360, velocidade=500)
wait(500)

# Mover 10 cm
robo.motor_local_cm("motor2", 10, diametro_roda=5.6, velocidade=500)
wait(500)

# Rodar continuamente
robo.motor_local_continuo("motor1", velocidade=600)
wait(3000)
robo.parar_motor_local("motor1")
wait(500)

# Invertendo direção
robo.motor_local_graus("motor2", -180, velocidade=400)
wait(500)

# Para todos
robo.parar_todos_motores_local()

print("✓ Concluído")
