"""R8 - Dançarino"""

from pybricks.parameters import Port, Color
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.adicionar_motor_local("motor_esq", Port.A)
robo.adicionar_motor_local("motor_dir", Port.B)

robo.luz_local(Color.CYAN)

for i in range(5):
    cmd = robo.receber_ble()
    tipo, valor, velocidade = cmd
    
    if tipo == "gira_direita":
        robo.motor_local_graus("motor_esq", valor, velocidade)
        robo.luz_local(Color.RED)
    elif tipo == "gira_esquerda":
        robo.motor_local_graus("motor_dir", valor, velocidade)
        robo.luz_local(Color.BLUE)
    elif tipo == "avancar":
        robo.motor_local_cm("motor_esq", valor, velocidade=velocidade)
        robo.motor_local_cm("motor_dir", valor, velocidade=velocidade)
        robo.luz_local(Color.GREEN)
    elif tipo == "recuar":
        robo.motor_local_cm("motor_esq", -valor, velocidade=velocidade)
        robo.motor_local_cm("motor_dir", -valor, velocidade=velocidade)
        robo.luz_local(Color.ORANGE)
    elif tipo == "pausa":
        wait(valor * 1000)
    
    robo.beep_local(1200, 100)
    wait(500)

robo.luz_local(Color.GREEN)
