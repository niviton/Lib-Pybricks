"""R3 - Provedor de sensores"""

from pybricks.parameters import Port, Color
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.adicionar_sensor_cor_local("cor", Port.D)
robo.adicionar_sensor_ultra_local("ultra", Port.C)

robo.luz_local(Color.CYAN)

for i in range(10):
    req = robo.receber_ble()
    
    if req == ("solicita_sensor",):
        reflexao = robo.ler_reflexao_local("cor")
        distancia = robo.ler_distancia_local("ultra")
        cor = robo.ler_cor_local("cor")
        
        dados = ("sensores", reflexao, distancia, cor)
        robo.enviar_ble(*dados)
        robo.beep_local(1000, 100)
    
    wait(500)

robo.luz_local(Color.GREEN)
