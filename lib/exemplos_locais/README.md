# 📚 Exemplos CNATMaker - Guia Completo

Bem-vindo! Aqui você encontra exemplos didáticos separados em **Locais** e **Remotos**.

## 🏠 Exemplos Locais (1 Hub Só)

Use estes para aprender o básico em um SPIKE Prime único.

### 01_led_e_som.py
**Aprenda:** Controlar LED, tocar sons, escrever na matriz
- Perfeito para: Primeiros passos
- Tempo: 5 min
- Comando: `pybricksdev run --name "hub 1" lib/exemplos_locais/01_led_e_som.py`

### 02_motores.py
**Aprenda:** Girar motores em graus, centímetros, continuamente
- Precisa de: 2 motores em Port A e B
- Tempo: 10 min
- Comando: `pybricksdev run --name "hub 1" lib/exemplos_locais/02_motores.py`

### 03_sensor_cor.py
**Aprenda:** Ler reflexão, HSV, detectar cores
- Precisa de: Sensor de cor em Port D
- Tempo: 15 min
- Comando: `pybricksdev run --name "hub 1" lib/exemplos_locais/03_sensor_cor.py`

### 04_sensor_ultra.py
**Aprenda:** Medir distância com ultrassom
- Precisa de: Sensor ultrassônico em Port C
- Tempo: 10 min
- Comando: `pybricksdev run --name "hub 1" lib/exemplos_locais/04_sensor_ultra.py`

### 05_giroscopio.py
**Aprenda:** Ler ângulos, girar com precisão
- Precisa de: 2 motores em Port A e B
- Tempo: 10 min
- Comando: `pybricksdev run --name "hub 1" lib/exemplos_locais/05_giroscopio.py`

### 06_seguidor_linha.py
**Aprenda:** Um projeto REAL - Robô seguidor de linha!
- Precisa de: 2 motores + sensor de cor
- Tempo: 20 min
- Comando: `pybricksdev run --name "hub 1" lib/exemplos_locais/06_seguidor_linha.py`

---

## 🌐 Exemplos Remotos (2 Hubs via Bluetooth)

Use estes para comunicação entre 2 SPIKE Prime.

### Como Executar Exemplos Remotos?

**SEMPRE em 2 TERMINAIS ao mesmo tempo:**

```powershell
# Terminal 1
pybricksdev run ble --name "hub 1" lib/exemplos_remotos/r1_hub1_transmissor.py

# Terminal 2 (outro PowerShell)
pybricksdev run ble --name "hub 2" lib/exemplos_remotos/r1_hub2_receptor.py
```

### r1_hub1_transmissor.py + r1_hub2_receptor.py
**Aprenda:** Enviar/receber mensagens entre hubs
- O que faz: Hub 1 envia 10 mensagens, Hub 2 recebe
- Verificar: Ambos printam confirmação
- Tempo: 15 min

### r2_hub1_controle.py + r2_hub2_executor.py
**Aprenda:** Hub 1 controla motor remotamente em Hub 2
- O que faz: Hub 1 envia comandos (girar, rodar, parar)
- Verificar: Motor em Hub 2 obedece os comandos
- Tempo: 20 min

---

## 📖 Ordem de Aprendizado Recomendada

```
┌─ INICIANTE
│  ├─ 01_led_e_som (entender output)
│  ├─ 02_motores (fazer algo se mover)
│  └─ 03_sensor_cor (ler informação)
│
├─ INTERMEDIÁRIO
│  ├─ 04_sensor_ultra (medir distância)
│  ├─ 05_giroscopio (controle preciso)
│  └─ 06_seguidor_linha (projeto completo com logic)
│
└─ AVANÇADO
   ├─ r1_*_transmissor/receptor (comunicação BLE)
   └─ r2_*_controle/executor (controle remoto)
```

---

## 🛠️ Função por Função

### LED e Som
```python
robo.luz_local(Color.GREEN)      # Mudar LED
robo.beep_local(1000, 200)       # Tocar som (freq, ms)
robo.mostrar_local("A")          # Mostrar letra
robo.limpar_display_local()      # Apagar display
```

### Motores
```python
robo.adicionar_motor_local("motor1", Port.A)
robo.motor_local_graus("motor1", 360)          # 1 volta
robo.motor_local_cm("motor1", 10)              # 10cm
robo.motor_local_continuo("motor1", 500)       # Rodar infinito
robo.parar_motor_local("motor1")               # Parar
robo.parar_todos_motores_local()               # Parar tudo
```

### Sensores
```python
# Cor
robo.adicionar_sensor_cor_local("cor", Port.D)
reflexao = robo.ler_reflexao_local("cor")      # 0-100
h, s, v = robo.ler_hsv_local("cor")            # Valores técnicos
cor = robo.ler_cor_local("cor")                # "AZUL", "VERMELHO"...
eh_azul = robo.eh_cor_local("cor", "AZUL")     # True/False
robo.calibrar_cor_local("cor", "meu_azul")    # Aprender nova cor

# Ultrassônico
robo.adicionar_sensor_ultra_local("ultra", Port.C)
distancia_mm = robo.ler_distancia_local("ultra")
distancia_cm = distancia_mm // 10

# Giroscópio
robo.resetar_giroscopio_local()                # Zerar posição
angulo = robo.ler_angulo_local()               # -180 a +180°
yaw, pitch, roll = robo.ler_orientacao_local() # 3D
robo.girar_ate_local(90)                       # Girar para ângulo
impacto = robo.detectar_impacto_local()        # True se bateu
```

### BLE (Multi-hub)
```python
robo.enviar_ble("hub1", "dados", 123)          # Enviar mensagem
msg = robo.receber_ble()                       # Receber mensagem
```

### Hub
```python
robo.esperar_botao_local()                     # Aguarda botão
robo.info()                                    # Mostra debug
```

---

## ❓ Perguntas Frequentes

**P: Por que o motor não funciona?**  
R: Verifique a porta (A, B, C, D) e se está realmente conectado.

**P: Sensor de cor sempre diz "DESCONHECIDO"?**  
R: Precisa calibrar! Use `calibrar_cor_local()` ou ajuste `cores_calibradas`.

**P: BLE não funciona?**  
R: Ambos hubs devem estar perto (< 10 metros). Reinicie os hubs.

**P: Como renomear um motor?**  
```python
# Isso está na linha:
robo.adicionar_motor_local("meu_motor", Port.A)
# Depois use:
robo.motor_local_graus("meu_motor", 360)
```

---

## 🚀 Próximas Ideias

Depois de aprender, tente:
- Robô que desvia de obstáculos (ultrassônico + motores)
- Detector de cor que aciona LED/som
- Braço robótico que gira com giroscópio
- Controle remoto com joystick (Hub 1) para motor (Hub 2)
- Sistema de alarme com detector de movimento

---

**Divirta-se! 🎉**
