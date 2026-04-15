"""R6 - Jogador 2"""

from pybricks.parameters import Color
from pybricks.tools import wait, StopWatch
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

input("Pressione ENTER para começar...")

robo.luz_local(Color.YELLOW)
robo.beep_local(800, 100)

timer = StopWatch()
contador = 0
tempo_limite = 10000
placar_p1 = None

def verificar_vencedor():
    global placar_p1
    try:
        msg = robo.receber_ble()
        if msg[0] == "botao":
            placar_p1 = msg[1]
    except:
        pass

while timer.time() < tempo_limite:
    verificar_vencedor()
    
    if robo.botao_pressionado_local():
        contador += 1
        robo.enviar_ble("botao", contador, timer.time())
        robo.beep_local(1000, 100)
        wait(300)

tempo_final = timer.time() / 1000.0
robo.luz_local(Color.GREEN)
