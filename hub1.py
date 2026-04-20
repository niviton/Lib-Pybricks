
from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.atuador.led.cor(Color.YELLOW)

robo.hub_configurar_porta("C2", "motor")

robo.atuador.motor.girar("C2", sentido="horario", rotacoes=1, potencia=80)
wait(5000)
robo.atuador.motor.girar("C2", sentido="anti_horario", rotacoes=0.5, potencia=80)
wait(5000)
robo.atuador.motor.arrancar("C2", sentido="horario", potencia=60)
wait(5000)
robo.atuador.motor.parar("C2")
wait(5000)

robo.atuador.led.cor(Color.GREEN)
print("✓ Sequencia remota finalizada")