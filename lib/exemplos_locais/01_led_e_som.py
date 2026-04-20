"""EXEMPLO 1: LED, Som e Display (API nova)"""

from pybricks.parameters import Color
from pybricks.tools import wait
from lib.CNATMake_lib import CNATMAKER_Bot

robo = CNATMAKER_Bot()

for cor in (Color.RED, Color.GREEN, Color.BLUE, Color.WHITE, Color.BLACK):
	robo.atuador.led.cor(cor)
	wait(400)

for freq in (262, 294, 330, 349):
	robo.atuador.som.beep(frequencia=freq, duracao=180)
	wait(250)

robo.atuador.display.mostrar("N")
wait(600)
robo.atuador.display.mostrar("W")
wait(600)
robo.limpar_display()

print("✓ Exemplo 1 finalizado")
