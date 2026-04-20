# Exemplos Locais - API Nova por Porta

Todos os exemplos desta pasta usam a API nova sem metodos local/remoto no codigo do usuario.

## Como executar

```powershell
pybricksdev run --name "hub 1" lib/exemplos_locais/01_led_e_som.py
```

Troque o arquivo no fim do comando para testar os outros.

## Arquivos

- 00_todas_funcoes_api_nova.py: demonstra as funcoes principais da nova API.
- 01_led_e_som.py: led, som e display.
- 02_motores.py: motor por porta (girar, arrancar, parar, posicao, velocidade).
- 03_sensor_cor.py: leitura e calibracao de cor por porta.
- 04_sensor_ultra.py: leitura de distancia por porta.
- 05_giroscopio.py: giroscopio + movimento.
- 06_seguidor_linha.py: projeto de linha com portas C e D para sensores.

## API usada nos exemplos

```python
robo.atuador.motor.girar(Port.A, sentido="horario", rotacoes=1, potencia=75)
robo.atuador.motor.arrancar(Port.A, sentido="horario", potencia=75)
robo.atuador.motor.ir_posicao(Port.A, posicao=0, sentido="curto", potencia=75)
robo.atuador.motor.parar(Port.A)
robo.atuador.motor.posicao(Port.A)
robo.atuador.motor.velocidade(Port.A)

robo.atuador.movimento.configurar(esq=Port.A, dir=Port.B, cm_por_rotacao=17.5)
robo.atuador.movimento.mover(sentido="frente", cm=10, potencia=75)
robo.atuador.movimento.arrancar(sentido="frente", potencia=75)
robo.atuador.movimento.girar(sentido="direita", graus=90, potencia=75)
robo.atuador.movimento.parar()

robo.atuador.display.mostrar("A")
robo.atuador.led.cor(Color.GREEN)
robo.atuador.som.beep(frequencia=1000, duracao=200)

robo.sensor.cor.ler(Port.D)
robo.sensor.cor.reflexao(Port.D)
robo.sensor.cor.calibrar(Port.D, "azul", segundos=5)
robo.sensor.distancia.ler(Port.C)
robo.sensor.giroscopio.angulo()
robo.sensor.giroscopio.resetar()

robo.hub.botao.pressionado()
robo.hub.bateria.voltagem()
```
