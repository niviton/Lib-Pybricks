"""R9 - Receptor avançado"""

from pybricks.parameters import Color
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.luz_local(Color.CYAN)

recebidos = []
for i in range(4):
    msg = robo.receber_ble()
    tipo = msg[0]
    
    if tipo in ("sensor", "status"):
        recebidos.append(msg)
        robo.enviar_ble("ack", i)
        robo.luz_local(Color.GREEN)
        robo.beep_local(1000, 100)
    else:
        robo.luz_local(Color.ORANGE)
    
    wait(500)

robo.luz_local(Color.GREEN)
