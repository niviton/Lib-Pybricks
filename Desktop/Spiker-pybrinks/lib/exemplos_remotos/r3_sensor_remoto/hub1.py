"""R3 - Solicitante de sensores"""

from pybricks.parameters import Color
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.luz_local(Color.YELLOW)

for i in range(10):
    robo.enviar_ble("solicita_sensor")
    
    resposta = robo.receber_ble()
    robo.beep_local(600, 100)
    wait(1000)

robo.luz_local(Color.GREEN)
print("\n✓ Coleta de dados remota completa!")
