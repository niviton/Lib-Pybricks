"""EXEMPLO 0: Todas as funcoes principais (API nova)"""

from pybricks.parameters import Port, Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

# Atuadores visuais/sonoros
robo.atuador.display.mostrar("A")
robo.atuador.led.cor(Color.GREEN)
robo.atuador.som.beep(frequencia=1000, duracao=120)
wait(300)

# Motor por porta
robo.atuador.motor.girar(Port.A, sentido="horario", rotacoes=0.5, potencia=70)
robo.atuador.motor.arrancar(Port.A, sentido="anti_horario", potencia=50)
wait(500)
robo.atuador.motor.parar(Port.A)
robo.atuador.motor.ir_posicao(Port.A, posicao=0, sentido="curto", potencia=60)
print("Posicao A:", robo.atuador.motor.posicao(Port.A))
print("Velocidade A:", robo.atuador.motor.velocidade(Port.A))

# Movimento (2 motores)
robo.atuador.movimento.configurar(esq=Port.A, dir=Port.B, cm_por_rotacao=17.5)
robo.atuador.movimento.mover(sentido="frente", cm=8, potencia=70)
wait(250)
robo.atuador.movimento.girar(sentido="direita", graus=45, potencia=70)
wait(250)
robo.atuador.movimento.arrancar(sentido="tras", potencia=50)
wait(400)
robo.atuador.movimento.parar()

# Sensores
print("Cor D:", robo.sensor.cor.ler(Port.D))
print("Reflexao D:", robo.sensor.cor.reflexao(Port.D))
print("Distancia C:", robo.sensor.distancia.ler(Port.C))
robo.sensor.giroscopio.resetar()
print("Angulo gyro:", robo.sensor.giroscopio.angulo())

# Hub
print("Botao pressionado:", robo.hub.botao.pressionado())
print("Voltagem bateria:", robo.hub.bateria.voltagem())

print("✓ Exemplo 0 finalizado")
