---
# Exemplos Remotos - 10 Projetos com 2 Hubs
---

## 📡 Comunicação Entre Hubs via Bluetooth

Use estes exemplos para dominar a comunicação entre 2 (ou mais) SPIKE Primes conectados via BLE!

---

## 🎯 Roteiro de Aprendizado

| # | Pasta | Hub 1 | Hub 2 | Tempo | Tema | Dific |
|---|-------|-------|-------|-------|------|-------|
| 🔴 | `r1_comunicacao_basica` | Transmite contador | Recebe contador | 15 min | Hello, BLE! | ⭐ |
| 🟠 | `r2_controle_motor` | Envia comandos motor | Executa mov | 20 min | Controle remoto | ⭐ |
| 🟡 | `r3_sensor_remoto` | Solicita dados | Envia sensores | 20 min | Coleta de dados | ⭐⭐ |
| 🟢 | `r4_led_remoto` | Envia cores | Exibe cores | 15 min | Sequência visual | ⭐ |
| 🔵 | `r5_botao_controle` | Detecta botão | Reage a evento | 15 min | EventListener | ⭐ |
| 🟣 | `r6_game_dois_jogadores` | Jogador 1 | Jogador 2 | 20 min | GAME - Corrida! | ⭐⭐ |
| 🔶 | `r7_sensores_distribuidos` | Agregador de dados | Provedor | 20 min | IoT Simples | ⭐⭐ |
| 🟤 | `r8_coordenacao_motores` | Maestro sinc | Dançarino | 25 min | Sincronização | ⭐⭐ |
| ⚪ | `r9_transmissao_dados` | Transmissor av | Receptor av | 20 min | Com verificar | ⭐⭐⭐ |
| ⚫ | `r10_projeto_completo` | Cérebro | Executor | 25 min | PROJETO REAL | ⭐⭐⭐ |

**Total:** ~170 minutos (~3 horas)

---

## 🚀 Como Executar

**Terminal 1 - Hub 1:**
```bash
cd c:\Users\Viviane\Desktop\Spiker-pybrinks
pybricksdev run ble --name "hub 1" lib/exemplos_remotos/r1_comunicacao_basica/hub1.py
```

**Terminal 2 - Hub 2:**
```bash
cd c:\Users\Viviane\Desktop\Spiker-pybrinks
pybricksdev run ble --name "hub 2" lib/exemplos_remotos/r1_comunicacao_basica/hub2.py
```

⚠️ **Importante:** Execute os 2 comandos **simultaneamente** em terminais diferentes!

---

## 📖 Detalhes de Cada Projeto

### R1: Comunicação Básica 🔴 ⭐
**Objetivo:** Seu primeiro programa BLE!

**Arquivos:**
- `hub1.py` - Transmite contador (0-9)
- `hub2.py` - Recebe contador e mostra

**Conceitos:**
- ✓ `enviar_ble(*dados)` 
- ✓ `receber_ble()` retorna tupla

**Output esperado:**
```
Hub 1:
[0] Enviando: ('contador', 0, 'segundos')
[1] Enviando: ('contador', 1, 'segundos')
...

Hub 2:
[0] Recebido: ('contador', 0, 'segundos')
[1] Recebido: ('contador', 1, 'segundos')
```

**Melhorias:**
- Adicione handshake de conexão
- Trate erros se desconectar

---

### R2: Controle Motor 🟠 ⭐
**Objetivo:** Hub 1 comanda movimento do Hub 2!

**Hardware necessário:**
- Hub 2: 1 motor em Porta A

**Mensagens (formato):**
```python
("motor", "graus", 90, 400)    # graus
("motor", "cm", 10, 300)       # centímetros
("motor", "continuo", 500, 2)  # 2 segundos continuo
("motor", "para", 0, 0)        # parar
```

**Casos de uso:**
- Robô controlado por segundo hub
- Comandos programados
- Sequência de movimentos

---

### R3: Sensor Remoto 🟡 ⭐⭐
**Objetivo:** Hub 1 questiona sensores do Hub 2!

**Hardware necessário:**
- Hub 2: Sensor cor (D) + Ultrassônico (C)

**Padrão Request/Response:**
```python
# Hub 1 envia
robo.enviar_ble("solicita_sensor")

# Hub 2 responde
dados = ("sensores", reflexao, distancia, cor)
robo.enviar_ble(*dados)
```

**Monitoramento remoto:**
- Supervisar estado do robô
- Coletar telemetria
- Validar funcionamento

---

### R4: LED Remoto 🟢 ⭐
**Objetivo:** Sequência de cores sincronizada!

**Mensagens:**
```python
("cor", Color.RED)    # manda cor
("cor", Color.BLUE)   # manda outra
```

**Casos de uso:**
- Status visual distribuído
- Feedback para usuário remoto
- Sincronização visual

---

### R5: Botão Controle 🔵 ⭐
**Objetivo:** Hub 1 detecta botão e Hub 2 reage!

**Fluxo:**
1. Você pressiona botão em Hub 1
2. Hub 1 envia evento
3. Hub 2 recebe e faz som/luz

**Padrão Event Listener:**
```python
if robo.botao_pressionado_local():
    robo.enviar_ble("botao", contador)
```

---

### R6: Game - Corrida 🟣 ⭐⭐
**Objetivo:** 🏆 PRIMEIRO GAME MULTIPLAYER!

**Regra:**
- Pressione botão 10x rapidamente
- Primeiro a completar vence
- Mostra placar

**Output:**
```
Jogador 1: 10 botões em 8.2s - VENCEU!
Jogador 2: 10 botões em 9.5s
```

**Experiência:**
Muito legal jogar contra amigo!

---

### R7: Sensores Distribuídos 🔶 ⭐⭐
**Objetivo:** Padrão IoT - Agregador coleta de múltiplos provedores

**Arquitetura:**
```
Hub 1 (Agregador)
  ↓ solicita_dados
Hub 2 (Provedor)
  ↑ resposta com sensores
```

**Escalável para:**
- Hub 1 = Gateway central
- Hub 2, 3, 4... = Sensores remotos

---

### R8: Coordenação de Motores 🟤 ⭐⭐
**Objetivo:** Dança sincronizada entre 2 robôs!

**Comandos de "dança":**
```python
("gira_direita", 180, 500)   # gira direita
("gira_esquerda", 180, 500)  # gira esquerda
("avancar", 10, 300)         # caminha frente
("recuar", 10, 300)          # caminha trás
("pausa", 2, 0)              # espera 2s
```

**Padrão Master/Slave:**
- Hub 1 = Maestro (envia tempo)
- Hub 2 = Dançarino (executa)

---

### R9: Transmissão com Verificação ⚪ ⭐⭐⭐
**Objetivo:** Troca confiável - confirmação de entrega!

**Padrão ACK (Acknowledge):**
```python
# Hub 1 envia
robo.enviar_ble("sensor", "temperatura", 35.5)

# Hub 2 valida e confirma
robo.enviar_ble("ack", 0)  # OK recebido
```

**Casos reais:**
- Comunicação crítica
- Dados que não podem se perder
- Validação de integridade

---

### R10: Projeto Completo ⚫ ⭐⭐⭐
**Objetivo:** 🏆 SISTEMA COMPLETO - Missão com 2 Hubs!

**Arquitetura:**
```
Hub 1 (Cérebro)
  • Sensor cor local
  • Decisões inteligentes
  • Coordena missão
  ↕ BLE
Hub 2 (Executora)
  • Motores
  • Executa comandos
  • Envia feedback
```

**Fases da missão:**
1. **Conexão** - Handshake
2. **Reconhecimento** - Hub 1 vê ambiente
3. **Comando** - Hub 1 ordena movimento
4. **Execução** - Hub 2 executa
5. **Verificação** - Hub 1 confirma sucesso
6. **Finalização** - Encerra com sucesso

**Output simulado:**
```
[Conectando]
✓ Conectado ao hub2

[Fase 1] Reconhecimento visual...
  Enviado: ('visao', 45, 'preto')

[Fase 2] Ordenando movimento...
  Comando: Avançar 15cm

[Fase 3] Verificando status...
  Status: ('status', 'ok', 1)

✓ Missão concluída!
```

---

## 🔧 Conceitos-Chave

### 1. Enviar Dados
```python
# Enviar múltiplos valores
robo.enviar_ble("tipo", valor1, valor2, valor3)

# Recebe como tupla no outro lado
msg = robo.receber_ble()  # ("tipo", valor1, valor2, valor3)
```

### 2. Request/Response
```python
# Hub A pede
hub_a.enviar_ble("solicita_dados")

# Hub B responde
dados = hub_b.receber_ble()
resposta = ("resposta", dados)
hub_b.enviar_ble(*resposta)

# Hub A recebe resposta
msg = hub_a.receber_ble()
```

### 3. Sinalizar Eventos
```python
# Hub 1 informa evento
if evento:
    robo.enviar_ble("evento", tipo, urgencia)

# Hub 2 reage
msg = robo.receber_ble()
if msg[0] == "evento":
    reage()
```

### 4. Handshake (Conexão segura)
```python
# Hub A inicia
hub_a.enviar_ble("conectar", "hub_a")

# Hub B confirma
msg = hub_b.receber_ble()
hub_b.enviar_ble("conectado", "hub_b")

# Hub A valida
msg = hub_a.receber_ble()
```

---

## 📊 Tabela de Canais BLE

| Hub | Canal | Nome | Padrão |
|-----|-------|------|--------|
| 1️⃣  | 24 | Hub 1 | LEGO SPIKE |
| 2️⃣  | 69 | Hub 2 | LEGO SPIKE |
| 3️⃣  | 32 | Hub 3 | LEGO SPIKE |

> Canais automáticos por nome!

---

## 🎓 Percurso Recomendado

**Dia 1:** R1 (hello BLE) + R4 (cores)  
**Dia 2:** R2 (motores) + R6 (game)  
**Dia 3:** R3 (sensores) + R7 (distribuído)  
**Dia 4:** R5 (botão) + R8 (dança)  
**Dia 5:** R9 (confiável) + R10 (projeto)  

---

## 🐛 Troubleshooting

### "Operation in progress"
Hub já conectado? Aguarde 5s e tente novamente.

### "Timed out waiting for device"
- [ ] Ambos hubs ligados?
- [ ] USB conectado?
- [ ] Digitou nome correto? (`--name "hub 1"`)

### Mensagem não chega
- [ ] Ambos rodando?
- [ ] Na mesma rede/área?
- [ ] Hubs reconhecem um ao outro?

### Port não encontrada
Força reiníciar:
```bash
pybricksdev connections list
pybricksdev connections forget <device>
```

---

## ✨ Ideias de Projetos Personalizados

1. **Jogo de Corrida** - Versão com obstáculos
2. **Siga-me** - Um hub segue o outro
3. **Coordenação de 3 hubs** - Orchestra!
4. **Controle remoto completo** - Todos os sensores
5. **Transmissão de temperatura** - Sensor remoto

---

## 📚 Referência Rápida

**Enviar:**
```python
robo.enviar_ble("tipo", valor1, valor2)
```

**Receber:**
```python
msg = robo.receber_ble()  # Retorna tupla
tipo, valor1, valor2 = msg
```

**Padrão de Loop:**
```python
while rodando:
    msg = robo.receber_ble()
    if msg[0] == "esperado":
        processar(msg)
```

---

## 🏆 Checklist de Aprendizado

- [ ] R1 - Consegue enviar/receber mensamens
- [ ] R2 - Hub 2 executa motores do Hub 1
- [ ] R3 - Hub 1 lê sensores remotos
- [ ] R4 - LEDs em sincronização
- [ ] R5 - Botão em um hub aciona outro
- [ ] R6 - Conseguiu vencer o game!
- [ ] R7 - Agregou dados de múltiplos
- [ ] R8 - Dança sincronizada funcionou
- [ ] R9 - Sistema com confirmação OK
- [ ] R10 - Missão completa funcionou

✅ **Parabéns!** Você domina BLE!

---

**Próximos passos:**
- Combine R10 com sua criatividade
- Crie interface em Python desktop
- Integre com smartphone/tablet
- Construa sistema de monitoramento real

**Bem-vindo ao mundo IoT com LEGO! 🚀**
