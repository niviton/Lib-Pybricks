"""R1 - Receptor simples"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.luz_local(Color.CYAN)

for i in range(10):
    msg = robo.receber_ble()
    robo.beep_local(1000, 100)
    wait(100)

robo.luz_local(Color.GREEN)
