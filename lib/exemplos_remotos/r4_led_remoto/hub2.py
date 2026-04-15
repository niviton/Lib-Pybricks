"""R4 - Exibidor de LED remoto"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

for i in range(8):
    msg = robo.receber_ble()
    tipo, cor = msg
    
    if tipo == "cor":
        robo.luz_local(cor)
        robo.beep_local(1200, 100)
    
    wait(100)

robo.luz_local(Color.GREEN)
