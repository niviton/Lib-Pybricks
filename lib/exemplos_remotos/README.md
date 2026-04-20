# Exemplos Remotos - API Nova por Porta

Todos os exemplos desta pasta usam apenas API por porta no codigo do usuario.

## Como executar

Abra dois terminais.

```powershell
# Terminal Hub 2
pybricksdev run ble --name "hub 2" lib/exemplos_remotos/r2_controle_motor/hub2.py

# Terminal Hub 1
pybricksdev run ble --name "hub 1" lib/exemplos_remotos/r2_controle_motor/hub1.py
```

Troque os caminhos para o exemplo desejado.

## Ordem recomendada

1. r1_comunicacao_basica
2. r2_controle_motor
3. r3_sensor_remoto
4. r8_coordenacao_motores
5. r10_projeto_completo

## Exemplo completo da API nova

Veja `r0_api_nova_completa` para um par hub1/hub2 que cobre:
- configuracao de portas remotas
- atuador.motor por porta remota
- atuador.movimento com duas portas remotas
- leitura de sensor.cor e sensor.distancia remotos
- hub.botao e atuador.led/som
