"""R9 - Transmissao de dados com ACK (Hub 1)"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.atuador.led.cor(Color.YELLOW)

dados = [
    ("sensor", "temperatura", 35.5),
    ("sensor", "umidade", 65),
    ("sensor", "pressao", 1013),
    ("status", "ok", 100),
]

for i, msg in enumerate(dados):
    robo.enviar_ble(*msg)
    robo.atuador.som.beep(frequencia=800, duracao=80)

    ack = robo.receber_ble()
    print("ACK esperado:", i, "| recebido:", ack)
    wait(500)

robo.atuador.led.cor(Color.GREEN)
