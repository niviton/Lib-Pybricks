"""
CNATMAKER_Bot - Biblioteca Completa para LEGO SPIKE Prime
===========================================================
Controla robôs single-hub (local) e multi-hub (remoto via BLE)

NOMES DAS FUNÇÕES:
  - _local() = funciona NO PRÓPRIO hub
  - _remoto() = funciona EM OUTRO hub via BLE
  - (sem sufixo) = versão legada (compatibilidade)

IDADE: 10 a 60+ anos (fácil de entender, nomes claros)
"""

from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction, Color
from pybricks.tools import wait, StopWatch


# ==========================================
# CONSTANTES
# ==========================================

DIAMETRO_RODA_PADRAO = 5.6
CIRCUNFERENCIA_PADRAO = DIAMETRO_RODA_PADRAO * 3.14159

CANAL_HUB1 = 24
CANAL_HUB2 = 69
CANAL_HUB3 = 32


# ==========================================
# CLASSE: CNATMAKER_Bot
# ==========================================

class CNATMAKER_Bot:
    """
    Classe principal para robôs LEGO SPIKE Prime
    Suporta motores, sensores de cor, ultrassônico, e giroscópio
    Detecta automaticamente multi-hub via BLE
    """
    
    def __init__(self):
        """Inicializa o robô"""
        print("\n" + "="*60)
        print("CNATMAKER_Bot v2.0 - Bem vindo!")
        print("="*60)
        
        self.hub = PrimeHub()
        self.nome_hub = self.hub.system.name()
        
        # Detectar configuração BLE
        self._detectar_hub()
        
        # Periféricos locais
        self.motores_locais = {}
        self.sensores_locais = {}
        
        # Calibração padrão de cores
        self.cores_calibradas = {
            "preto":    {"h": (0, 360), "s": (0, 30), "v": (0, 20)},
            "cinza":    {"h": (0, 360), "s": (0, 20), "v": (40, 60)},
            "branco":   {"h": (0, 360), "s": (0, 20), "v": (80, 100)},
            "vermelho": {"h": (345, 10), "s": (80, 100), "v": (40, 100)},
            "amarelo":  {"h": (45, 65), "s": (50, 100), "v": (60, 100)},
            "verde":    {"h": (110, 150), "s": (50, 100), "v": (30, 80)},
            "ciano":    {"h": (170, 200), "s": (50, 100), "v": (50, 100)},
            "azul":     {"h": (210, 250), "s": (50, 100), "v": (50, 100)},
            "magenta":  {"h": (280, 320), "s": (50, 100), "v": (50, 100)}
        }
        
        print(f"[Bot] Hub: {self.nome_hub}")
        print(f"[Bot] Bateria: {self.hub.battery.voltage()}mV")
        print("="*60 + "\n")
        
        # Animação de boas-vindas
        self.mostrar_local("M")
        wait(100)
        self.mostrar_local("A")
        wait(100)
        self.mostrar_local("k")
        wait(100)
        self.mostrar_local("E")
        wait(100)
        self.mostrar_local("R")
        wait(500)
        self.limpar_display_local()
    
    def _detectar_hub(self):
        """Detecta qual hub está rodando"""
        nome = self.nome_hub.lower()
        
        if "hub 1" in nome or "spike0" in nome:
            self.canal_tx = CANAL_HUB1
            self.canais_rx = [CANAL_HUB2, CANAL_HUB3]
            self.modo_ble = "servidor"
        elif "hub 2" in nome or "spike1" in nome:
            self.canal_tx = CANAL_HUB2
            self.canais_rx = [CANAL_HUB1, CANAL_HUB3]
            self.modo_ble = "cliente"
        else:
            self.canal_tx = CANAL_HUB3
            self.canais_rx = [CANAL_HUB1, CANAL_HUB2]
            self.modo_ble = "cliente"
        
        # Tentar inicializar BLE
        try:
            self.hub = PrimeHub(
                broadcast_channel=self.canal_tx,
                observe_channels=self.canais_rx
            )
            print(f"[Bot] ✓ BLE OK (TX: {self.canal_tx})")
        except:
            print(f"[Bot] BLE não disponível (single-hub)")
    
    # ==========================================
    # INTERFACE HUB: LED, SOM, DISPLAY
    # ==========================================
    
    def luz_local(self, cor):
        """Muda cor do LED do botão
        Ex: robo.luz_local(Color.GREEN)
        """
        self.hub.light.on(cor)
    
    def beep_local(self, frequencia=1000, duracao_ms=200):
        """Toca som no speaker
        Ex: robo.beep_local(1000, 100)
        """
        self.hub.speaker.beep(frequencia, duracao_ms)
    
    def mostrar_local(self, texto):
        """Mostra 1 caractere na matriz 5×5
        Ex: robo.mostrar_local("A")
        """
        if texto:
            self.hub.display.text(texto[0])
    
    def limpar_display_local(self):
        """Apaga matriz de LEDs"""
        self.hub.display.off()
    
    def botao_pressionado_local(self):
        """Retorna True se botão está pressionado AGORA
        Ex: if robo.botao_pressionado_local(): ...
        """
        return self.hub.buttons.pressed()
    
    def esperar_botao_local(self, timeout_ms=10000):
        """Aguarda pressionar o botão central
        Ex: robo.esperar_botao_local()
        """
        print("[Bot] Pressione o botão para começar...")
        self.luz_local(Color.YELLOW)
        self.mostrar_local("?")
        
        relogio = StopWatch()
        while relogio.time() < timeout_ms:
            if self.hub.buttons.pressed():
                self.limpar_display_local()
                self.luz_local(Color.GREEN)
                self.beep_local(1000, 100)
                wait(300)
                return True
            wait(50)
        
        return False
    
    # ==========================================
    # MOTORES: Registrar
    # ==========================================
    
    def adicionar_motor_local(self, nome, porta, direcao=Direction.CLOCKWISE):
        """Registra um motor local
        
        Ex:
            robo.adicionar_motor_local("esquerdo", Port.A)
            robo.adicionar_motor_local("direito", Port.B, Direction.COUNTERCLOCKWISE)
        """
        try:
            motor = Motor(porta, direcao)
            self.motores_locais[nome] = {
                "motor": motor,
                "nome": nome,
                "porta": porta
            }
            print(f"[Bot] ✓ Motor '{nome}' em {porta}")
            return True
        except Exception as e:
            print(f"[Bot] ✗ Erro no motor '{nome}': {e}")
            return False
    
    # ==========================================
    # MOTORES: Controlar
    # ==========================================
    
    def motor_local_graus(self, nome, graus, velocidade=500):
        """Roda motor X graus
        
        Ex:
            robo.motor_local_graus("direito", 360)        # 1 volta
            robo.motor_local_graus("esquerdo", -180, 300) # meia volta inversa
        """
        if nome not in self.motores_locais:
            print(f"[Bot] Motor '{nome}' não encontrado")
            return
        
        motor = self.motores_locais[nome]["motor"]
        motor.run_angle(velocidade, graus)
    
    def motor_local_cm(self, nome, cm, diametro_roda=DIAMETRO_RODA_PADRAO, velocidade=500):
        """Roda motor X centímetros (para rodas)
        
        Ex:
            robo.motor_local_cm("direito", 10)  # move 10cm
            robo.motor_local_cm("direito", -5)  # move 5cm pra trás
        """
        circunferencia = diametro_roda * 3.14159
        graus = (cm / circunferencia) * 360
        self.motor_local_graus(nome, graus, velocidade)
    
    def motor_local_continuo(self, nome, velocidade=500):
        """Roda motor CONTINUAMENTE (até parar_motor_local)
        
        Ex:
            robo.motor_local_continuo("esquerdo", 500)
            wait(2000)
            robo.parar_motor_local("esquerdo")
        """
        if nome not in self.motores_locais:
            print(f"[Bot] Motor '{nome}' não encontrado")
            return
        
        motor = self.motores_locais[nome]["motor"]
        motor.run(velocidade)
    
    def parar_motor_local(self, nome):
        """Para um motor específico
        
        Ex:
            robo.parar_motor_local("esquerdo")
        """
        if nome not in self.motores_locais:
            return
        
        motor = self.motores_locais[nome]["motor"]
        motor.stop()
    
    def parar_todos_motores_local(self):
        """Para TODOS os motores
        
        Ex:
            robo.parar_todos_motores_local()
        """
        for nome in self.motores_locais:
            self.parar_motor_local(nome)
    
    # ==========================================
    # SENSORES COR: Registrar
    # ==========================================
    
    def adicionar_sensor_cor_local(self, nome, porta):
        """Registra um sensor de cor local
        
        Ex:
            robo.adicionar_sensor_cor_local("cor", Port.D)
        """
        try:
            sensor = ColorSensor(porta)
            self.sensores_locais[nome] = {
                "sensor": sensor,
                "tipo": "COR",
                "porta": porta
            }
            print(f"[Bot] ✓ Sensor cor '{nome}' em {porta}")
            return True
        except Exception as e:
            print(f"[Bot] ✗ Erro no sensor '{nome}': {e}")
            return False
    
    # ==========================================
    # SENSORES COR: Ler valores
    # ==========================================
    
    def ler_reflexao_local(self, nome):
        """Lê REFLEXÃO (0-100) - para seguidor de linha
        
        Ex:
            reflexao = robo.ler_reflexao_local("cor")
            if reflexao > 50:
                print("Superfície clara")
        """
        if nome not in self.sensores_locais:
            return 0
        
        sensor = self.sensores_locais[nome]["sensor"]
        return sensor.reflection()
    
    def ler_hsv_local(self, nome):
        """Lê HSV (Hue, Saturation, Value) da cor
        Retorna: (H, S, V)
        
        Ex:
            h, s, v = robo.ler_hsv_local("cor")
            print(f"Hue: {h}°, Saturation: {s}%, Value: {v}%")
        """
        if nome not in self.sensores_locais:
            return (0, 0, 0)
        
        sensor = self.sensores_locais[nome]["sensor"]
        hsv = sensor.hsv()
        return (hsv.h, hsv.s, hsv.v)
    
    def ler_cor_local(self, nome):
        """Lê cor e retorna nome (ex: "AZUL", "VERMELHO")
        
        Ex:
            cor = robo.ler_cor_local("cor")
            if cor == "AZUL":
                print("Detectei azul!")
        """
        h, s, v = self.ler_hsv_local(nome)
        
        # Detecção simples
        for cor_nome, lims in self.cores_calibradas.items():
            h_min, h_max = lims["h"]
            s_min, s_max = lims["s"]
            v_min, v_max = lims["v"]
            
            # Verificar wrap-around (vermelho em 0-10 e 350-360)
            if h_min > h_max:
                h_ok = (h >= h_min or h <= h_max)
            else:
                h_ok = (h_min <= h <= h_max)
            
            s_ok = (s_min <= s <= s_max)
            v_ok = (v_min <= v <= v_max)
            
            if h_ok and s_ok and v_ok:
                return cor_nome.upper()
        
        return "DESCONHECIDO"
    
    def eh_cor_local(self, nome, cor_esperada):
        """Verifica se a cor é uma específica
        
        Ex:
            if robo.eh_cor_local("cor", "AZUL"):
                print("É azul mesmo!")
        """
        return self.ler_cor_local(nome) == cor_esperada.upper()
    
    def calibrar_cor_local(self, nome, nome_cor, tempo_s=5):
        """Calibra cores automaticamente aprendendo os valores
        
        Ex:
            robo.calibrar_cor_local("cor", "meu_azul", tempo_s=5)
        """
        print(f"\n[Bot] Calibrando '{nome_cor}' por {tempo_s}s...")
        print("[Bot] Aponte o sensor para a cor...")
        
        relogio = StopWatch()
        h_vals = []
        s_vals = []
        v_vals = []
        
        while relogio.time() < tempo_s * 1000:
            h, s, v = self.ler_hsv_local(nome)
            h_vals.append(h)
            s_vals.append(s)
            v_vals.append(v)
            print(f"H:{h:3d} S:{s:3d} V:{v:3d}  ", end="\r")
            wait(100)
        
        h_min, h_max = min(h_vals), max(h_vals)
        s_min, s_max = min(s_vals), max(s_vals)
        v_min, v_max = min(v_vals), max(v_vals)
        
        self.cores_calibradas[nome_cor.lower()] = {
            "h": (h_min, h_max),
            "s": (s_min, s_max),
            "v": (v_min, v_max)
        }
        
        print(f"\n✓ Calibração guardada!")
        print(f'"{nome_cor}": {{"h": ({h_min}, {h_max}), "s": ({s_min}, {s_max}), "v": ({v_min}, {v_max})}}\n')
    
    # ==========================================
    # SENSORES ULTRASSÔNICO: Registrar
    # ==========================================
    
    def adicionar_sensor_ultra_local(self, nome, porta):
        """Registra sensor ultrassônico local
        
        Ex:
            robo.adicionar_sensor_ultra_local("ultra", Port.C)
        """
        try:
            sensor = UltrasonicSensor(porta)
            self.sensores_locais[nome] = {
                "sensor": sensor,
                "tipo": "ULTRA",
                "porta": porta
            }
            print(f"[Bot] ✓ Sensor ultra '{nome}' em {porta}")
            return True
        except Exception as e:
            print(f"[Bot] ✗ Erro no sensor '{nome}': {e}")
            return False
    
    # ==========================================
    # SENSORES ULTRASSÔNICO: Ler
    # ==========================================
    
    def ler_distancia_local(self, nome):
        """Lê DISTÂNCIA em milímetros (mm)
        
        Ex:
            dist_mm = robo.ler_distancia_local("ultra")
            dist_cm = dist_mm // 10
            if dist_cm < 20:
                print("Objeto perto!")
        """
        if nome not in self.sensores_locais:
            return 2000
        
        sensor = self.sensores_locais[nome]["sensor"]
        try:
            return sensor.distance()
        except:
            return 2000
    
    # ==========================================
    # GIROSCÓPIO / IMU (Movimento 3D)
    # ==========================================
    
    def resetar_giroscopio_local(self):
        """Zera o giroscópio (define posição atual como 0°)
        
        Ex:
            robo.resetar_giroscopio_local()
        """
        self.hub.imu.reset_heading(0)
        print("[Bot] ✓ Giroscópio resetado")
    
    def ler_angulo_local(self):
        """Lê ângulo de rotação (YAW) em graus (-180 a +180)
        
        Ex:
            angulo = robo.ler_angulo_local()
            print(f"Virado para: {angulo}°")
        """
        return self.hub.imu.heading()
    
    def ler_orientacao_local(self):
        """Lê 3 eixos: (yaw, pitch, roll)
        
        Ex:
            yaw, pitch, roll = robo.ler_orientacao_local()
        """
        yaw = self.hub.imu.heading()
        pitch, roll = self.hub.imu.tilt()
        return (yaw, pitch, roll)
    
    def ler_aceleracao_local(self):
        """Lê aceleração em 3 eixos (mm/s²)
        
        Ex:
            x, y, z = robo.ler_aceleracao_local()
        """
        return self.hub.imu.acceleration()
    
    def girar_ate_local(self, angulo_alvo, velocidade=50):
        """Gira o robô até um ângulo específico
        
        Ex:
            robo.girar_ate_local(90)   # Gira 90° à direita
            robo.girar_ate_local(-90)  # Gira 90° à esquerda
        """
        print(f"[Bot] Girando para {angulo_alvo}°...")
        
        # Precisa ter motores nomeados "esquerdo" e "direito"
        if "esquerdo" not in self.motores_locais or "direito" not in self.motores_locais:
            print("[Bot] ✗ Motores 'esquerdo' e 'direito' necessários")
            return
        
        relogio = StopWatch()
        timeout = 30000  # 30 segundos máximo
        
        while relogio.time() < timeout:
            angulo_atual = self.ler_angulo_local()
            erro = angulo_alvo - angulo_atual
            
            # Normalizar erro para -180 a +180
            if erro > 180:
                erro -= 360
            elif erro < -180:
                erro += 360
            
            if abs(erro) < 2:
                break
            
            # Controle proporcional
            vel = max(-100, min(100, int(erro * 3 / 100))) * 10
            
            self.motor_local_continuo("esquerdo", vel)
            self.motor_local_continuo("direito", -vel)
            
            wait(50)
        
        self.parar_todos_motores_local()
        print(f"[Bot] ✓ Girado para {self.ler_angulo_local()}°")
    
    def detectar_impacto_local(self, sensibilidade=2500):
        """Detecta se o robô foi batido/colidiu
        
        Ex:
            if robo.detectar_impacto_local():
                print("OUCH! Levei uma pancada!")
        """
        x, y, z = self.ler_aceleracao_local()
        return (abs(x) + abs(y) + abs(z)) > sensibilidade
    
    # ==========================================
    # BLE: Comunicação Multi-Hub
    # ==========================================
    
    def enviar_ble(self, *dados):
        """Envia dados via BLE para outro hub
        
        Ex:
            robo.enviar_ble("hub1", "cor", "AZUL", 50)
        """
        try:
            self.hub.ble.broadcast(data=dados)
            return True
        except Exception as e:
            print(f"[Bot] Erro BLE: {e}")
            return False
    
    def receber_ble(self):
        """Recebe dados via BLE
        
        Ex:
            msg = robo.receber_ble()
            if msg:
                print(f"Recebi: {msg}")
        """
        try:
            return self.hub.ble.observe(channel=self.canais_rx[0])
        except:
            return None
    
    # ==========================================
    # INFORMAÇÕES
    # ==========================================
    
    def info(self):
        """Mostra informações do robô"""
        print("\n" + "="*60)
        print("INFORMAÇÕES DO ROBÔ")
        print("="*60)
        print(f"Hub: {self.nome_hub}")
        print(f"Bateria: {self.hub.battery.voltage()}mV")
        print(f"\nMotores: {len(self.motores_locais)}")
        for nome in self.motores_locais:
            print(f"  • {nome}")
        print(f"\nSensores: {len(self.sensores_locais)}")
        for nome, info in self.sensores_locais.items():
            print(f"  • {nome} ({info['tipo']})")
        print("="*60 + "\n")
    
    
    # ==========================================
    # FUNÇÕES LEGADAS (COMPATIBILIDADE)
    # ==========================================
    
    def adicionar_motor(self, nome, porta, direcao=Direction.CLOCKWISE):
        return self.adicionar_motor_local(nome, porta, direcao)
    
    def adicionar_sensor_cor(self, nome, porta):
        return self.adicionar_sensor_cor_local(nome, porta)
    
    def adicionar_sensor_ultra(self, nome, porta):
        return self.adicionar_sensor_ultra_local(nome, porta)
    
    def motor_graus(self, nome, graus, velocidade=500):
        return self.motor_local_graus(nome, graus, velocidade)
    
    def motor_cm(self, nome, cm, diametro=DIAMETRO_RODA_PADRAO, velocidade=500):
        return self.motor_local_cm(nome, cm, diametro, velocidade)
    
    def motor_continuo(self, nome, velocidade=500):
        return self.motor_local_continuo(nome, velocidade)
    
    def parar_motor(self, nome):
        return self.parar_motor_local(nome)
    
    def parar_todos(self):
        return self.parar_todos_motores_local()
    
    def ler_cor(self, nome):
        return self.ler_cor_local(nome)
    
    def ler_distancia(self, nome):
        return self.ler_distancia_local(nome)
    
    def luz(self, cor):
        return self.luz_local(cor)
    
    def beep(self, freq=1000, ms=200):
        return self.beep_local(freq, ms)


# ==========================================
# Atalho
# ==========================================

def criar_robo():
    """Cria e retorna um novo robô
    Ex: robo = criar_robo()
    """
    return CNATMAKER_Bot()
