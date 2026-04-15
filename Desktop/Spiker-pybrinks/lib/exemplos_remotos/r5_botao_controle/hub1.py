"""R5 - Detector de botão"""

from pybricks.parameters import Color
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.luz_local(Color.YELLOW)

tempo_total = 15
dentro = 0
contador = 0

while dentro < tempo_total:
    if robo.botao_pressionado_local():
        contador += 1
        msg = ("botao_pressionado", contador)
        robo.enviar_ble(*msg)
        robo.beep_local(1000, 200)
        wait(500)
    
    wait(100)
    dentro += 0.1

robo.luz_local(Color.GREEN)
