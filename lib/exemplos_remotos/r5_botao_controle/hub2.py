"""R5 - Reagidor a botão remoto"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.luz_local(Color.CYAN)

for i in range(15):
    try:
        msg = robo.receber_ble()
        tipo, numero = msg
        
        if tipo == "botao_pressionado":
            robo.luz_local(Color.ORANGE)
            robo.beep_local(1200, 150)
            wait(300)
            robo.luz_local(Color.CYAN)
    except:
        pass
    
    wait(1000)

robo.luz_local(Color.GREEN)
