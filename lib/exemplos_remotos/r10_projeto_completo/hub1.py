"""R10 - Cérebro do robô"""

from pybricks.parameters import Color, Port
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.adicionar_sensor_cor_local("cor", Port.D)
robo.luz_local(Color.YELLOW)

robo.enviar_ble("conectar", "hub1")
try:
    resp = robo.receber_ble()
except:
    pass

reflexao = robo.ler_reflexao_local("cor")
cor = robo.ler_cor_local("cor")

msg_visao = ("visao", reflexao, cor)
robo.enviar_ble(*msg_visao)
robo.beep_local(800, 100)
wait(1000)

robo.enviar_ble("movimento", "avancar", 15)
robo.beep_local(900, 150)
wait(2000)

robo.enviar_ble("solicita_status")
try:
    status = robo.receber_ble()
except:
    pass

robo.enviar_ble("finalizar", "hub1")
robo.luz_local(Color.GREEN)
