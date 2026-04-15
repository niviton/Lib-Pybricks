"""R1 - Transmissor de contador"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.luz_local(Color.YELLOW)

for i in range(10):
    msg = ("contador", i, "segundos")
    robo.enviar_ble(*msg)
    robo.beep_local(800, 100)
    wait(1000)

robo.luz_local(Color.GREEN)
