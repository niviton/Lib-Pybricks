"""R2 - Executor de motor"""

from pybricks.parameters import Port, Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.adicionar_motor_local("motor", Port.A)

robo.luz_local(Color.CYAN)

for i in range(4):
    cmd = robo.receber_ble()
    
    if cmd[0] == "motor":
        if cmd[1] == "graus":
            robo.motor_local_graus(cmd[0], cmd[2], cmd[3])
        elif cmd[1] == "cm":
            robo.motor_local_cm(cmd[0], cmd[2], velocidade=cmd[3])
        elif cmd[1] == "continuo":
            robo.motor_local_continuo(cmd[0], cmd[2])
            wait(cmd[3] * 1000)
            robo.parar_motor_local(cmd[0])
        elif cmd[1] == "para":
            robo.parar_motor_local(cmd[0])
    
    robo.beep_local(1000, 100)
    wait(500)

robo.luz_local(Color.GREEN)
