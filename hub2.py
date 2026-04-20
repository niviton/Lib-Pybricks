"""HUB 2 - TEMPLATE OFICIAL (copie e rode)"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

# Detecta automaticamente motores e sensores conectados no Hub 2.
robo.configurar_hardware_automatico()
robo.atuador.led.cor(Color.CYAN)

while True:
    # Executa comandos de atuadores recebidos do Hub 1.
    pacote = robo.receber_ble_rapido()
    if pacote:
        robo.executar_ble_rapido(pacote)

    # Publica sensores continuamente para leitura por porta no Hub 1.
    robo.transmitir_stream_sensores()
    wait(1)
