"""CLIENTE - Hub 2 (SLAVE)"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

# ====== COPIE E COLE SEU CÓDIGO AQUI ======
# Cole o código do exemplo que quer rodar
# Exemplo: copiar tudo de exemplos_locais/02_motores.py

robo.luz_local(Color.BLUE)
robo.beep_local(800, 100)

print("Cliente iniciado")

# Seu código aqui
wait(2000)

robo.luz_local(Color.GREEN)

print("✓ Cliente finalizado")
       