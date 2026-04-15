"""SERVIDOR - Hub 1 (MASTER)"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

# ====== COPIE E COLE SEU CÓDIGO AQUI ======
# Cole o código do exemplo que quer rodar
# Exemplo: copiar tudo de exemplos_locais/01_led_e_som.py

# Mostrar no display

robo.esperar_botao_local()
robo.limpar_display_local()

robo.luz_local(Color.GREEN)

print("✓ Servidor finalizado")
