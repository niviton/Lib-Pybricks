"""EXEMPLO 5: Giroscópio"""

from pybricks.parameters import Port, Direction
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.adicionar_motor_local("esquerdo", Port.A)
robo.adicionar_motor_local("direito", Port.B, Direction.COUNTERCLOCKWISE)

# Resetar giroscópio
robo.resetar_giroscopio_local()

# Ler ângulo (10 vezes)
print("Lendo ângulo...")
for i in range(10):
    angulo = robo.ler_angulo_local()
    print(f"  [{i}] {angulo}°")
    wait(500)

# Ler orientação 3D
print("\nLendo orientação 3D...")
for i in range(5):
    yaw, pitch, roll = robo.ler_orientacao_local()
    print(f"  [{i}] Yaw:{yaw}° Pitch:{pitch}° Roll:{roll}°")
    wait(500)

# Detectar impactos (10 vezes)
print("\nDetectando impactos...")
for i in range(10):
    if robo.detectar_impacto_local():
        print(f"  Batida detectada!")
        robo.beep_local(1000, 100)
    wait(500)

# Girar até 90°
print("\nGirando até 90°...")
wait(2000)
robo.girar_ate_local(90, velocidade=50)
angulo_final = robo.ler_angulo_local()
print(f"Ângulo final: {angulo_final}°")

print("✓ Concluído")
