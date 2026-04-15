"""R7 - Agregador de dados"""

from pybricks.parameters import Color
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.luz_local(Color.YELLOW)

tempo_coleta = 10
dentro = 0

while dentro < tempo_coleta:
    robo.enviar_ble("solicita_dados")
    
    try:
        dados_hub2 = robo.receber_ble()
    except:
        pass
    
    wait(1000)
    dentro += 1

robo.luz_local(Color.GREEN)
