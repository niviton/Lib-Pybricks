# Lib-Pybricks - CNATMAKER Bot

Biblioteca didatica para LEGO SPIKE Prime com API nova baseada em porta.

## API padrao

Use sempre chamadas por porta, sem separar local/remoto no codigo de usuario.

```python
robo.atuador.motor.girar("A2", sentido="horario", rotacoes=1, potencia=75)
robo.sensor.cor.reflexao("D1")
robo.sensor.distancia.ler("C2")
robo.atuador.movimento.configurar(esq="A2", dir="B2", cm_por_rotacao=17.5)
robo.hub.botao.pressionado()
```

## Requisitos

1. Python 3.11+
2. pybricksdev instalado
3. Hubs SPIKE com nomes coerentes (ex: hub 1, hub 2)

## Instalacao

```powershell
pip install pybricksdev
```

## Estrutura

```text
Lib-Pybricks/
├── lib/
│   ├── CNATMake_lib.py
│   ├── exemplos_locais/
│   │   ├── 00_todas_funcoes_api_nova.py
│   │   ├── 01_led_e_som.py
│   │   ├── 02_motores.py
│   │   ├── 03_sensor_cor.py
│   │   ├── 04_sensor_ultra.py
│   │   ├── 05_giroscopio.py
│   │   ├── 06_seguidor_linha.py
│   │   └── README.md
│   └── exemplos_remotos/
│       ├── r0_api_nova_completa/
│       │   ├── hub1.py
│       │   └── hub2.py
│       ├── r1_comunicacao_basica/
│       ├── r2_controle_motor/
│       ├── r3_sensor_remoto/
│       ├── r4_led_remoto/
│       ├── r5_botao_controle/
│       ├── r6_game_dois_jogadores/
│       ├── r7_sensores_distribuidos/
│       ├── r8_coordenacao_motores/
│       ├── r9_transmissao_dados/
│       ├── r10_projeto_completo/
│       └── README.md
├── hub1.py
├── hub2.py
└── README.md
```

## Como executar

### Exemplo local

```powershell
pybricksdev run --name "hub 1" lib/exemplos_locais/00_todas_funcoes_api_nova.py
```

### Exemplo remoto

```powershell
# Terminal 1 (Hub 2)
pybricksdev run ble --name "hub 2" lib/exemplos_remotos/r0_api_nova_completa/hub2.py

# Terminal 2 (Hub 1)
pybricksdev run ble --name "hub 1" lib/exemplos_remotos/r0_api_nova_completa/hub1.py
```

## Funcoes principais

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

## Guias detalhados

- `lib/exemplos_locais/README.md`
- `lib/exemplos_remotos/README.md`

## Observacoes

1. No VS Code local pode aparecer aviso de import `pybricks.*` nao resolvido. Isso e esperado fora do runtime do Hub.
2. Em remoto, suba primeiro o `hub2.py` e depois o `hub1.py`.
