"""EXEMPLO 3: Sensor de Cor"""

from pybricks.parameters import Port
from pybricks.tools import wait

from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.adicionar_sensor_cor_local("cor", Port.D)

# Ler reflexão (10 vezes)
print("Lendo reflexão...")
for i in range(10):
    reflexao = robo.ler_reflexao_local("cor")
    print(f"  [{i}] {reflexao}%")
    wait(500)

# Ler HSV
print("\nLendo HSV...")
for i in range(5):
    h, s, v = robo.ler_hsv_local("cor")
    print(f"  H:{h}° S:{s}% V:{v}%")
    wait(500)

# Detectar cores
print("\nDetectando cores (10s)...")
cores_vistas = set()
for _ in range(20):
    cor = robo.ler_cor_local("cor")
    cores_vistas.add(cor)
    wait(500)

print(f"Cores: {', '.join(sorted(cores_vistas))}")

# Verificar cor
if robo.eh_cor_local("cor", "AZUL"):
    print("É AZUL!")
else:
    print("Não é azul")

print("✓ Concluído")
