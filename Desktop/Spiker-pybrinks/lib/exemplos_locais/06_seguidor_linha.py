"""
EXEMPLO 6: Seguidor de Linha com 2 Sensores
"""

from pybricks.parameters import Port, Direction, Color
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

# Configurar motores
robo.adicionar_motor_local("esquerdo", Port.A)
robo.adicionar_motor_local("direito", Port.B, Direction.COUNTERCLOCKWISE)

# Configurar sensores
robo.adicionar_sensor_cor_local("cor_esq", Port.C)
robo.adicionar_sensor_cor_local("cor_dir", Port.D)

print("Pressione botão para começar...")
robo.esperar_botao_local()

robo.luz_local(Color.GREEN)

RAPIDA = 80
LENTA = 40
LIMIAR = 50

# Executar por 30 segundos
for _ in range(600):
    esq = robo.ler_reflexao_local("cor_esq") < LIMIAR
    dir = robo.ler_reflexao_local("cor_dir") < LIMIAR
    
    # Ambos na linha = reto
    if esq and dir:
        robo.motor_local_continuo("esquerdo", RAPIDA)
        robo.motor_local_continuo("direito", RAPIDA)
    # Esquerdo na linha = vira direita
    elif esq:
        robo.motor_local_continuo("esquerdo", RAPIDA)
        robo.motor_local_continuo("direito", LENTA)
    # Direito na linha = vira esquerda
    elif dir:
        robo.motor_local_continuo("esquerdo", LENTA)
        robo.motor_local_continuo("direito", RAPIDA)
    # Nenhum na linha = para
    else:
        robo.parar_todos_motores_local()
    
    wait(50)

robo.parar_todos_motores_local()
robo.luz_local(Color.RED)
print("✓ Concluído")
