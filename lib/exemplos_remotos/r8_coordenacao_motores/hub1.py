"""R8 - Maestro de sincronização"""

from pybricks.parameters import Color
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.luz_local(Color.YELLOW)

movimentos = [
    ("gira_direita", 180, 500),
    ("gira_esquerda", 180, 500),
    ("avancar", 10, 300),
    ("recuar", 10, 300),
    ("pausa", 2, 0),
]

for idx, (tipo, valor, velocidade) in enumerate(movimentos):
    robo.enviar_ble(tipo, valor, velocidade)
    robo.beep_local(800, 100)
    wait(2000)

robo.luz_local(Color.GREEN)
