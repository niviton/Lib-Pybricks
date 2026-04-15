---
# Exemplos Locais - Guia Completo (Atualizado)
---

## 📚 10 Exemplos Progre

ssivos para Aprender

Domine a programação do **SPIKE Prime** seguindo esta sequência didática.  
Cada exemplo build incrementalmente. ⏱️ Total: ~60 minutos.

---

## 🚀 Roteiro Recomendado

| # | Arquivo | Tempo | Tema | Dificuldade | Pré-req |
|---|---------|-------|------|-------------|---------|
| 1️⃣ | `01_led_e_som.py` | 5 min | LED + Som | ⭐ Iniciante | Nenhum |
| 2️⃣ | `02_motores.py` | 10 min | Controlar Motores | ⭐ Iniciante | Ex. 1 |
| 3️⃣ | `03_sensor_cor.py` | 15 min | Cores e Calibração | ⭐ Iniciante | Ex. 1 |
| 4️⃣ | `04_sensor_ultra.py` | 10 min | Distância | ⭐⭐ Intermediário | Ex. 2 |
| 5️⃣ | `05_giroscopio.py` | 10 min | Rotação Precisa | ⭐⭐ Intermediário | Ex. 2 |
| 6️⃣ | `06_seguidor_linha.py` | 20 min | Projeto: Linha | ⭐⭐ Intermediário | Ex. 2,3 |
| 7️⃣ | `07_desvio_obstaculos.py` | 15 min | Robô Autônomo | ⭐⭐ Intermediário | Ex. 2,4 |
| 8️⃣ | `08_braco_robotico.py` | 15 min | Braço 3 Motores | ⭐⭐ Intermediário | Ex. 2 |
| 9️⃣ | `09_multiplos_sensores.py` | 15 min | Monitorar Tudo | ⭐⭐⭐ Avançado | Ex. 3,4,5 |
| 🔟 | `10_botao_multiplos_modos.py` | 12 min | Máquina Estados | ⭐⭐⭐ Avançado | Todos |

---

## 📖 Detalhes de Cada Exemplo

### Exemplo 1: LED e Som ⭐
**Objetivo:** Primeiro programa! Controlar o LED e fazer sons.

**Componentes necessários:**
- Hub SPIKE Prime (nenhum periférico!)

**Conceitos aprendidos:**
- ✓ Importar a biblioteca
- ✓ Criar instância do robô
- ✓ Controlar cores do LED
- ✓ Fazer beeps

**Comando para executar:**
```bash
pybricksdev run --name "hub 1" lib/exemplos_locais/01_led_e_som.py
```

**🎯 Melhoria sugerida:**
Faça uma sequência de cores tipo de semáforo!

---

### Exemplo 2: Motores ⭐
**Objetivo:** Aprender a controlar motores em graus e centímetros.

**Componentes necessários:**
- Motores em Porta A e B

**Conceitos aprendidos:**
- ✓ Adicionar motores
- ✓ Rotação em graus
- ✓ Movimento em centímetros  
- ✓ Rotação contínua
- ✓ Parar motor

**Método importante - `motor_local_graus()`:**
```python
robo.motor_local_graus("nome", graus, velocidade)
```

**Método importante - `motor_local_cm()`:**
```python
robo.motor_local_cm("nome", cm, diametro_roda=5.6, velocidade)
```

---

### Exemplo 3: Sensor de Cor ⭐
**Objetivo:** Ler e calibrar o sensor de cor.

**Componentes necessários:**
- Sensor de Cor em Porta D

**Conceitos aprendidos:**
- ✓ Ler reflexão
- ✓ Ler HSV
- ✓ Detectar cor nomeada
- ✓ Calibrar novas cores

**Calibração manual:**
```python
robo.calibrar_cor_local("cor", "vermelho", tempo_s=3)
```

**⚠️ Importante:** Já vem com 9 cores pré-calibradas!

---

### Exemplo 4: Sensor Ultrassônico ⭐⭐
**Objetivo:** Medir distância de objetos.

**Componentes necessários:**
- Sensor ultrassônico em Porta C

**Conceitos aprendidos:**
- ✓ Ler distância em mm
- ✓ Converter para cm
- ✓ Usar para lógica de desvio

**Retorna valor em milímetros:**
```python
dist_mm = robo.ler_distancia_local("ultra")
```

---

### Exemplo 5: Giroscópio ⭐⭐
**Objetivo:** Rotações precisas usando o giroscópio.

**Componentes necessários:**
- Hub com giroscópio integrado

**Conceitos aprendidos:**
- ✓ Resetar ângulo
- ✓ Ler heading (yaw)
- ✓ Girar até ângulo específico
- ✓ Detectar impacto

**Método importante:**
```python
robo.girar_ate_local(180, velocidade=400)  # Gira até 180°
```

---

### Exemplo 6: Seguidor de Linha ⭐⭐
**Objetivo:** 🏆 **PROJETO REAL** - Robô segue uma linha!

**Montagem necessária:**
```
      [Hub]
       |
    ---|---
   |  Sensor Cor
   A Motor L
   B Motor R
   D Cor
```

**Lógica simples:**
- Se vê **preto** → segue (motor rápido)
- Se vê **branco** → corrige (motor lento)

**Rotina de teste:**
1. Desenhe linha preta em fundo branco
2. Coloque robô **sobre a linha**
3. Execute e veja desviar!

---

### Exemplo 7: Desvio de Obstáculos ⭐⭐
**Objetivo:** Robô autônomo que explora e desvia!

**Hardware:**
- 2 motores (esquerdo/direito)
- Sensor ultrassônico

**Algoritmo:**
```
while tempo < 30s:
    dist = ler_distancia()
    if dist < 15cm:
        desviar()  # Ré + giro
    else:
        avancar()  # Frente
```

**Experiência prática:**
Coloque em espaço aberto (1m x 1m) e veja explorar!

---

### Exemplo 8: Braço Robótico ⭐⭐
**Objetivo:** Controlar 3 motores sincronizados (braço com garra).

**Hardware necessário:**
- Port A: Base (gira)
- Port B: Cotovelo (levanta/abaixa)
- Port C: Garra (abre/fecha)

**Posições pré-programadas:**
- Repouso
- Buscar
- Pegar
- Levantar
- Virar esquerda/direita

**Melhorias:**
- Adicionar sensor de força
- Controle via BLE (ver R8)

---

### Exemplo 9: Múltiplos Sensores ⭐⭐⭐
**Objetivo:** Monitorar vários sensores simultaneamente.

**Aprenda a:**
- ✓ Ler vários dados de uma vez
- ✓ Tomar decisões complexas
- ✓ Detectar mudanças rápidas

**Output de exemplo:**
```
Tempo | Cor       | Reflexão | Distância | Ângulo
0001s | preto     | 25%      | 150mm     | 45°
0002s | branco    | 75%      | 500mm     | 46°
```

---

### Exemplo 10: Máquina de Estados ⭐⭐⭐
**Objetivo:** Implementar sistema com múltiplos modos.

**Modos disponíveis:**
1. **LIGAR** - Motor girando (manual)
2. **AUTO** - Seguidor de linha (automático)
3. **TESTE** - Mostra dados de sensores
4. **DESLIGAR** - Repouso

**Padrão de design importante:**
```python
while rodando:
    modo = modos[modo_atual % len(modos)]
    
    if modo == "LIGAR":
        # fazer algo
    elif modo == "AUTO":
        # outra coisa
    elif modo == "TESTE":
        # teste
    elif modo == "DESLIGAR":
        # repouso
```

---

## 🔧 Configurações Comuns

### Adicionar Motor
```python
robo.adicionar_motor_local("nome_único", Port.A, Direction.COUNTERCLOCKWISE)
```

### Adicionar Sensor Cor
```python
robo.adicionar_sensor_cor_local("cor", Port.D)
```

### Adicionar Sensor Ultrassônico
```python
robo.adicionar_sensor_ultra_local("ultra", Port.C)
```

### Diâmetro da Roda
```python
# Padrão SPIKE: 5.6 cm
diametro = 5.6  # customize se necessário
robo.motor_local_cm("motor", 10, diametro_roda=diametro, velocidade=300)
```

---

## 🎓 Ordem de Estudo Recomendada

**Semana 1 (Iniciante):**
- Dia 1: Exemplo 1 (LED)
- Dia 2: Exemplo 2 (Motores)
- Dia 3: Exemplo 3 (Cor)

**Semana 2 (Intermediário):**
- Dia 1: Exemplo 4 (Ultrassônico)
- Dia 2: Exemplo 5 (Giroscópio)
- Dia 3: Exemplo 6 (Seguidor) ← PROJETO!

**Semana 3 (Avançado):**
- Dia 1: Exemplo 7 (Desvio)
- Dia 2: Exemplo 8 (Braço)
- Dia 3: Exemplo 9 (Multi-sensor)

**Semana 4 (Proje Specialto):**
- Dia 1: Exemplo 10 (Máquina Estados)
- Dia 2-3: Crie seu próprio projeto!

---

## 🐛 Troubleshooting

### "Module not found: CNATMake_lib"
**Solução:** Verifique que você está executando do diretório correto:
```bash
cd c:\Users\Viviane\Desktop\Spiker-pybrinks
pybricksdev run --name "hub 1" lib/exemplos_locais/01_led_e_som.py
```

### Motor não responde
**Checklist:**
- [ ] Motor está plugado?
- [ ] Porta está correta (A, B, C, D)?
- [ ] Hub está ligado?
- [ ] ID único do motor é diferente dos outros?

### Sensor não detecta cor
**Checklist:**
- [ ] Sensor está limpo?
- [ ] Luz ambiente está normal?
- [ ] Sensor está calibrado?

### "Timed out waiting for BLE"
- Ambos os hubs ligados?
- Rodando no mesmo ambiente?

---

## 📚 Referência Rápida de Funções

### Motor
- `motor_local_graus(nome, graus, velocidade)`
- `motor_local_cm(nome, cm, diametro_roda=5.6, velocidade)`
- `motor_local_continuo(nome, velocidade)`
- `parar_motor_local(nome)`
- `parar_todos_motores_local()`

### Cor
- `ler_reflexao_local(nome)` → 0-100%
- `ler_hsv_local(nome)` → (H, S, V)
- `ler_cor_local(nome)` → cor nomeada
- `eh_cor_local(nome, cor)` → verdadeiro/falso
- `calibrar_cor_local(nome, nome_cor, tempo_s)`

### Ultrassônico
- `ler_distancia_local(nome)` → mm

### Giroscópio
- `resetar_giroscopio_local()`
- `ler_angulo_local()` → -180 a +180°
- `ler_orientacao_local()` → (yaw, pitch, roll)
- `ler_aceleracao_local()` → (x, y, z)
- `girar_ate_local(angulo, velocidade)`
- `detectar_impacto_local(sensibilidade)`

### Hub
- `luz_local(Color.nome)` 
- `beep_local(frequencia, duracao_ms)`
- `mostrar_local(texto)` - caractere matrix
- `limpar_display_local()`
- `botao_pressionado_local()` → True/False
- `esperar_botao_local(timeout_ms)`

---

## 🏆 Próximos Passos

1. **Domine os 10 exemplos** - Faça cada um funcionar
2. **Combine ideias** - Misture conceitos de diferentes exemplos
3. **Crie seu projeto** - Use como base os exemplos
4. **Compartilhe** - Mostre seus projetos para os amigos!

---

**Bom aprendizado! 🚀**

> Dúvidas? Revise o código de cada exemplo - está muito comentado!
