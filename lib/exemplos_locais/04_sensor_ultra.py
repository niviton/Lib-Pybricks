"""EXEMPLO 4: Sensor Ultrassônico"""

from pybricks.parameters import Port
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

robo.adicionar_sensor_ultra_local("ultra", Port.C)

# Ler distância (10 vezes)
print("Lendo distância...")
for i in range(10):
    dist_mm = robo.ler_distancia_local("ultra")
    dist_cm = dist_mm // 10
    print(f"  [{i}] {dist_mm}mm = {dist_cm}cm")
    wait(500)

# Detectar objetos próximos (10 segundos)
print("\nDetectando objetos próximos...")
distancia_limite = 20
objetos = 0

for _ in range(20):
    dist_cm = robo.ler_distancia_local("ultra") // 10
    if dist_cm < distancia_limite:
        print(f"Objeto detectado: {dist_cm}cm")
        objetos += 1
        wait(1000)
    else:
        wait(500)

print(f"Total: {objetos} objeto(s)")

print("✓ Concluído")
