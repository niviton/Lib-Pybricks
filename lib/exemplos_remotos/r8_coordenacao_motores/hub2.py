"""R8 - Hub 2 multiplexador automatico"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()
robo.configurar_hardware_automatico()
robo.atuador.led.cor(Color.CYAN)

while True:
    pacote = robo.receber_ble_rapido()
    if pacote:
        robo.executar_ble_rapido(pacote)

    robo.transmitir_stream_sensores()
    wait(1)
