"""R2 - Controlador de motor"""

from pybricks.parameters import Color
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.luz_local(Color.YELLOW)

comandos = [
    ("motor", "graus", 90, 400),
    ("motor", "cm", 10, 300),
    ("motor", "continuo", 500, 2),
    ("motor", "para", 0, 0),
]

for cmd in comandos:
    robo.enviar_ble(*cmd)
    robo.beep_local(800, 150)
    wait(1000)

robo.luz_local(Color.GREEN)
print("\n✓ Sequência de controle enviada!")
