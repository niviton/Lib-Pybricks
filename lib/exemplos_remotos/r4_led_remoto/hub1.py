"""R4 - Controlador de LED remoto"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.luz_local(Color.YELLOW)

cores_sequencia = [
    ("cor", Color.RED),
    ("cor", Color.ORANGE),
    ("cor", Color.YELLOW),
    ("cor", Color.GREEN),
    ("cor", Color.CYAN),
    ("cor", Color.BLUE),
    ("cor", Color.PURPLE),
    ("cor", Color.WHITE),
]

for i, (tipo, cor) in enumerate(cores_sequencia):
    robo.enviar_ble(tipo, cor)
    robo.beep_local(900, 100)
    wait(800)

robo.luz_local(Color.GREEN)
