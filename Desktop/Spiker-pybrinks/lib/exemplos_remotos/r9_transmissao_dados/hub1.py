"""R9 - Transmissor avançado"""

from pybricks.parameters import Color
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.luz_local(Color.YELLOW)

dados = [
    ("sensor", "temperatura", 35.5),
    ("sensor", "umidade", 65),
    ("sensor", "pressao", 1013),
    ("status", "ok", 100),
]

enviados = 0
for idx, msg in enumerate(dados):
    robo.enviar_ble(*msg)
    robo.beep_local(800, 100)
    
    try:
        ack = robo.receber_ble()
        if ack == ("ack", idx):
            enviados += 1
    except:
        pass
    
    wait(1000)

robo.luz_local(Color.GREEN)
