# 🤖 Spiker-PyBrinks - CNATMAKER Bot

Biblioteca completa e didática para programar **LEGO SPIKE Prime**.

> Para uso educacional de 10 a 60+ anos

---

## 📦 Estrutura do Projeto

```
Spiker-pybrinks/
├── lib/
│   ├── CNATMake_lib.py           ← BIBLIOTECA PRINCIPAL
│   ├── __init__.py
│   ├── exemplos_locais/          ← Aprender o básico (1 hub)
│   │   ├── 01_led_e_som.py
│   │   ├── 02_motores.py
│   │   ├── 03_sensor_cor.py
│   │   ├── 04_sensor_ultra.py
│   │   ├── 05_giroscopio.py
│   │   ├── 06_seguidor_linha.py
│   │   └── README.md             ← GUIA COMPLETO
│   └── exemplos_remotos/         ← Multi-hub via BLE
│       ├── r1_hub1_transmissor.py
│       ├── r1_hub2_receptor.py
│       ├── r2_hub1_controle.py
│       └── r2_hub2_executor.py
├── cliente.py                    ← Seu projeto Hub 2
├── servidor.py                   ← Seu projeto Hub 1
└── README.md                     ← Este arquivo
```

---

## 🚀 Começar Rápido

### 1️⃣ Executar um Exemplo Local

1. Abra terminal PowerShell
2. Escolha um exemplo em `lib/exemplos_locais/`
3. Execute:

```powershell
pybricksdev run --name "hub 1" lib/exemplos_locais/01_led_e_som.py
```

### 2️⃣ Aprender com Exemplos Remotos (2 Hubs)

1. Abra **2 TerminalesPowerShell**
2. **Terminal 1:**
```powershell
pybricksdev run ble --name "hub 1" lib/exemplos_remotos/r1_hub1_transmissor.py
```

3. **Terminal 2:**
```powershell
pybricksdev run ble --name "hub 2" lib/exemplos_remotos/r1_hub2_receptor.py
```

---

## 📚 Aprender por Nível

### 🟢 INICIANTE (Sem conhecimento prévio)

1. **01_led_e_som.py** - Fazer o LED piscar (5 min)
2. **02_motores.py** - Fazer rodas girar (10 min)
3. **03_sensor_cor.py** - Detectar cores (15 min)

### 🟡 INTERMEDIÁRIO (Conceitos básicos)

4. **04_sensor_ultra.py** - Medir distância (10 min)
5. **05_giroscopio.py** - Girar com precisão (10 min)
6. **06_seguidor_linha.py** - Projeto REAL (20 min)

### 🔴 AVANÇADO (Lógica complexa)

7. **r1_*_transmissor/receptor.py** - BLE simples (15 min)
8. **r2_*_controle/executor.py** - Controle remoto (20 min)

---

## 💡 Funções Principais

### 🎨 LED e Som
```python
from pybricks.parameters import Color

robo.luz_local(Color.GREEN)          # Led verde
robo.beep_local(1000, 200)           # Som 1000Hz por 200ms
robo.mostrar_local("A")              # Escrever na matriz
```

### ⚙️ Motores
```python
from pybricks.parameters import Port, Direction

robo.adicionar_motor_local("motor1", Port.A)
robo.motor_local_graus("motor1", 360)         # Girar 1 volta
robo.motor_local_cm("motor1", 10)             # Mover 10cm
robo.motor_local_continuo("motor1", 500)      # Rodar infinito
robo.parar_motor_local("motor1")              # Parar
```

### 🎨 Sensores
```python
from pybricks.parameters import Port

# Cor
robo.adicionar_sensor_cor_local("cor", Port.D)
reflexao = robo.ler_reflexao_local("cor")           # 0-100
cor = robo.ler_cor_local("cor")                     # "AZUL", "VERMELHO"
robo.eh_cor_local("cor", "AZUL")                    # True/False
robo.calibrar_cor_local("cor", "meu_azul")        # Aprender nova cor

# Ultrassônico
robo.adicionar_sensor_ultra_local("ultra", Port.C)
distancia = robo.ler_distancia_local("ultra") // 10  # em cm

# Giroscópio
robo.resetar_giroscopio_local()                     # Zerar
angulo = robo.ler_angulo_local()                    # -180 a +180°
robo.girar_ate_local(90)                            # Girar para 90°
```

### 📡 Bluetooth (Multi-hub)
```python
robo.enviar_ble("hub1", "dados", 123)   # Enviar
msg = robo.receber_ble()                # Receber
```

### 🎮 Controle
```python
robo.esperar_botao_local()              # Aguarda botão
robo.botao_pressionado_local()          # Verifica se pressionado agora
robo.info()                             # Mostra debug
```

---

## 📖 Documentação Completa

Veja **`lib/exemplos_locais/README.md`** para:
- Descri cao de cada exemplo
- Ordem de aprendizado
- Tabela de funções
- FAQ e troubleshooting

---

## 🔧 Seus Projetos

- **`cliente.py`** - Use este arquivo para seu projeto no Hub 2
- **`servidor.py`** - Use este arquivo para seu projeto no Hub 1

Exemplo:
```python
# servidor.py (Hub 1)
from lib.CNATMake_lib import CNATMAKER_Bot
from pybricks.parameters import Port, Color

robo = CNATMAKER_Bot()
robo.adicionar_motor_local("motor1", Port.A)
robo.motor_local_graus("motor1", 360)
```

---

## ⚠️ Troubleshooting

| Problema | Solução |
|----------|---------|
| Motor não funciona | Verifique porta (A, B, C, D) e conexão física |
| Sensor de cor diz "DESCONHECIDO" | Calibre com `calibrar_cor_local()` |
| BLE não conecta | Aproxime os hubs e reinicie |
| Código não executa | Verifique nome do hub com `--name` |

---

## 🎯 Objetivos de Aprendizado

Após completion dos exemplos, você será capaz de:

✅ Controlar motores com precisão (graus/cm)
✅ Ler diversos sensores (cor, distância, movimento)
✅ Calibrar sensores para funcionar melhor
✅ Criar loops com lógica (if/else)
✅ Comunicar entre 2 hubs via Bluetooth
✅ Construir projetos REAIS (seguidor de linha, robô autônomo)

---

## 📞 Suporte

**Não funciona?**
1. Leia `lib/exemplos_locais/README.md`
2. Verifique as conexões físicas
3. Reinicie os hubs
4. Tente um exemplo mais simples primeiro

---

**Divirta-se criando com SPIKE Prime! 🚀**
