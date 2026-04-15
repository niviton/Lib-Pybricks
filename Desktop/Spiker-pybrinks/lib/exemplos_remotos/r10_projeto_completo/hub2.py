"""R10 - Executora da missão"""

from pybricks.parameters import Color, Port
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.adicionar_motor_local("esq", Port.A)
robo.adicionar_motor_local("dir", Port.B)
robo.luz_local(Color.CYAN)

msg = robo.receber_ble()
if msg[0] == "conectar":
    robo.enviar_ble("conectado", "hub2")

rodando = True
missao_fases = 0

while rodando:
    try:
        cmd = robo.receber_ble()
        
        if cmd[0] == "visao":
            reflexao, cor = cmd[1], cmd[2]
            robo.luz_local(Color.PURPLE)
        
        elif cmd[0] == "movimento":
            tipo, valor = cmd[1], cmd[2]
            
            if tipo == "avancar":
                robo.motor_local_cm("esq", valor)
                robo.motor_local_cm("dir", valor)
                robo.luz_local(Color.GREEN)
            elif tipo == "recuar":
                robo.motor_local_cm("esq", -valor)
                robo.motor_local_cm("dir", -valor)
                robo.luz_local(Color.ORANGE)
            
            missao_fases += 1
            robo.beep_local(1200, 100)
        
        elif cmd[0] == "solicita_status":
            status_msg = ("status", "ok", missao_fases)
            robo.enviar_ble(*status_msg)
        
        elif cmd[0] == "finalizar":
            robo.parar_todos_motores_local()
            rodando = False
        
        wait(100)
    
    except:
        pass

robo.luz_local(Color.GREEN)
