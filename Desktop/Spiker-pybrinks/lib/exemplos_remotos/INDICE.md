---
# 📡 ÍNDICE DE EXEMPLOS REMOTOS
---

## 📂 Estrutura de Pastas

```
exemplos_remotos/
├── r1_comunicacao_basica/
│   ├── hub1.py            ← Começa aqui!
│   └── hub2.py
├── r2_controle_motor/
│   ├── hub1.py
│   └── hub2.py
├── r3_sensor_remoto/
│   ├── hub1.py
│   └── hub2.py
├── r4_led_remoto/
│   ├── hub1.py
│   └── hub2.py
├── r5_botao_controle/
│   ├── hub1.py
│   └── hub2.py
├── r6_game_dois_jogadores/
│   ├── hub1.py            ← GAME!
│   └── hub2.py
├── r7_sensores_distribuidos/
│   ├── hub1.py
│   └── hub2.py
├── r8_coordenacao_motores/
│   ├── hub1.py            ← DANÇA!
│   └── hub2.py
├── r9_transmissao_dados/
│   ├── hub1.py
│   └── hub2.py
├── r10_projeto_completo/
│   ├── hub1.py            ← PROJETO REAL!
│   └── hub2.py
└── README_REMOTOS.md      ← Leia depois
```

---

## 🚀 Início Rápido

**Opção 1: Copie e Cole (Windows PowerShell)**

```powershell
# Terminal 1
cd "c:\Users\Viviane\Desktop\Spiker-pybrinks"
pybricksdev run ble --name "hub 1" lib/exemplos_remotos/r1_comunicacao_basica/hub1.py

# Terminal 2
cd "c:\Users\Viviane\Desktop\Spiker-pybrinks"
pybricksdev run ble --name "hub 2" lib/exemplos_remotos/r1_comunicacao_basica/hub2.py
```

---

## 🎯 Qual Exemplo Escolher?

| Pergunta | Resposta | Exemplo |
|----------|----------|---------|
| Quero entender BLE básico? | Sim | **R1** |
| Quero controlar motor remoto? | Sim | **R2** |
| Quero ler sensores remotos? | Sim | **R3** |
| Quero fazer cores blincar? | Sim | **R4** |
| Quero reagir a botão remoto? | Sim | **R5** |
| Quero jogar contra alguém? | Sim | **R6** 🎮 |
| Quero coletar dados de sensores? | Sim | **R7** |
| Quero sincronizar movimentos? | Sim | **R8** 🎵 |
| Quero sistema confiável? | Sim | **R9** |
| Quero ver tudo junto? | Sim | **R10** 🏆 |

---

## 📋 Lista Completa

### R1 - Comunicação Básica
- **Tempo:** 15 minutos
- **Conceito:** Enviar/Receber mensagens simples
- **Arquivos:** `hub1.py`, `hub2.py`
- **Start:** Hub 1 envia contador, Hub 2 recebe
- **Output:** Números 0-9 trocando
- **Próximo:** R2

### R2 - Controle Motor
- **Tempo:** 20 minutos
- **Conceito:** Hub 1 comanda movimento Hub 2
- **Hardware:** 1 motor em Hub 2
- **Arquivos:** `hub1.py`, `hub2.py`
- **Comando:** Graus, CM, Contínuo, Para
- **Próximo:** R3

### R3 - Sensor Remoto
- **Tempo:** 20 minutos
- **Conceito:** Request/Response de sensores
- **Hardware:** Cor (D) + Ultra (C) em Hub 2
- **Arquivos:** `hub1.py`, `hub2.py`
- **Padrão:** Hub 1 solicita → Hub 2 responde
- **Próximo:** R4 ou R5

### R4 - LED Remoto
- **Tempo:** 15 minutos
- **Conceito:** Sequência de cores
- **Arquivos:** `hub1.py`, `hub2.py`
- **Visual:** Arco-íris de cores syncronizado
- **Próximo:** R5

### R5 - Botão Controle
- **Tempo:** 15 minutos
- **Conceito:** Event Listener
- **Arquivos:** `hub1.py`, `hub2.py`
- **Fluxo:** Botão → BLE → Reação
- **Próximo:** R6

### R6 - Game (Corrida)
- **Tempo:** 20 minutos
- **Conceito:** Multiplayer competitivo
- **Arquivos:** `hub1.py`, `hub2.py`
- **Regra:** 10 cliques mais rápido = vence
- **Diversão:** ⭐⭐⭐⭐⭐
- **Próximo:** R7

### R7 - Sensores Distribuídos
- **Tempo:** 20 minutos
- **Conceito:** Padrão IoT simples
- **Arquivos:** `hub1.py`, `hub2.py`
- **Padrão:** Agregador + Provedor de dados
- **Escalável:** Prototipagem de projetos IoT
- **Próximo:** R8

### R8 - Coordenação (Dança)
- **Tempo:** 25 minutos
- **Conceito:** Master/Slave sincronização
- **Arquivos:** `hub1.py`, `hub2.py`
- **Visual:** Movimento sincronizado
- **Criativo:** Grande potencial! 🎵
- **Próximo:** R9

### R9 - Transmissão Confiável
- **Tempo:** 20 minutos
- **Conceito:** Confirmação de entrega (ACK)
- **Arquivos:** `hub1.py`, `hub2.py`
- **Robusto:** Para comunicação crítica
- **Padrão:** Indústria de telecomunicações
- **Próximo:** R10

### R10 - Projeto Completo
- **Tempo:** 25 minutos
- **Conceito:** Sistema integrado
- **Arquivos:** `hub1.py`, `hub2.py`
- **Fases:** 6 etapas de missão completa
- **Real:** Aplicável em produção
- **Final:** Dominou BLE! 🏆

---

## 💡 Tabela de Padrões

| Padrão | Exemplo | Uso |
|--------|---------|-----|
| **Broadcast** | R1, R4 | Enviar para todos |
| **Request/Response** | R3, R7, R9 | Conversa de perguntas |
| **Event Listener** | R5 | Reagir a eventos |
| **Master/Slave** | R2, R8 | Um controla outro |
| **Multiplayer** | R6 | Vários jogadores |
| **Agregador** | R7, R10 | Coleta central |
| **Handshake** | R10 | Validar conexão |

---

## 🔗 Ordem de Execução Recomendada

1. **Iniciante (Primeira sessão - 1 hora)**
   ```
   R1 → R4 → R5
   ```
   Resultado: Entende send/receive + LED + Botão

2. **Intermediário (Segunda sessão - 1.5 horas)**
   ```
   R2 → R6 → R7
   ```
   Resultado: Motor remoto + Game + IoT básico

3. **Avançado (Terceira sessão - 1.5 horas)**
   ```
   R3 → R8 → R9
   ```
   Resultado: Sensores + Coordenação + Confiabilidade

4. **Expert (Quarta sessão - 30 min)**
   ```
   R10
   ```
   Resultado: Sistema completo e profissional

---

## 🎓 Timeline Sugerida

**Semana 1:**
- Seg: R1 + R4
- Qua: R2 + R5
- Sex: R3 + R6

**Semana 2:**
- Seg: R7 + R8
- Qua: R9 + R10
- Sex: Seu projeto próprio!

---

## ✅ Checklist

- [ ] R1 - Enviou/recebeu números
- [ ] R2 - Motor remoto funcionou
- [ ] R3 - Leu sensores remotos
- [ ] R4 - Cores em sequência
- [ ] R5 - Botão acionou outro hub
- [ ] R6 - Jogou gato contra amigo
- [ ] R7 - Agregou dados
- [ ] R8 - Deu uma "dança" sincronizada
- [ ] R9 - Sistema confiável OK
- [ ] R10 - Missão se completou

🎉 **Parabéns! Você é especialista em BLE com LEGO!**

---

## 🚀 Próximas Ideias

1. Combine R10 + Smartphone
2. Integre com Dashboard web
3. Sensor de temperatura remoto
4. Vigilância com câmera
5. Robô autônomo controlado remotamente

---

**Comece com R1 agora! 📡**
