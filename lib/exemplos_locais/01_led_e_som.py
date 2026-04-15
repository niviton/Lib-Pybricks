"""EXEMPLO 1: LED e Som"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

# Sequência de cores
wait(500)
robo.luz_local(Color.RED)
wait(500)
robo.luz_local(Color.GREEN)
wait(500)
robo.luz_local(Color.BLUE)
wait(500)
robo.luz_local(Color.BLACK)

# Tocar sons
robo.beep_local(262, 200)
wait(300)
robo.beep_local(294, 200)
wait(300)
robo.beep_local(330, 200)
wait(300)
robo.beep_local(349, 200)

# Mostrar no display
robo.mostrar_local("H")
wait(1000)
robo.mostrar_local("I")
wait(1000)
robo.limpar_display_local()

print("✓ Concluído")
