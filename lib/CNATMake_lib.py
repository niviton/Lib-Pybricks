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

# Protocolo rapido BLE (binario)
BLEFAST_MAGIC = 0xA7

BLEFAST_CMD_CONTINUO = 1
BLEFAST_CMD_PARAR = 2
BLEFAST_CMD_GRAUS = 3
BLEFAST_CMD_CM = 4

BLEFAST_SENTIDO_FRENTE = 1
BLEFAST_SENTIDO_TRAS = 2

BLESTREAM_MAGIC = 0xB4
BLESTREAM_TIPO_COR_REFLEXAO = 1
BLESTREAM_TIPO_DISTANCIA = 2


class _HubBotaoFacade:
    def __init__(self, robo):
        self.robo = robo

    def pressionado(self):
        return bool(self.robo.botao_pressionado_local())


class _HubBateriaFacade:
    def __init__(self, robo):
        self.robo = robo

    def voltagem(self):
        return int(self.robo._hub_hw.battery.voltage())


class _HubFacade:
    def __init__(self, robo):
        self.robo = robo
        self.botao = _HubBotaoFacade(robo)
        self.bateria = _HubBateriaFacade(robo)

    def __getattr__(self, nome):
        # Mantem compatibilidade com PrimeHub: robo.hub.light, robo.hub.ble, etc.
        return getattr(self.robo._hub_hw, nome)


class _AtuadorMotorFacade:
    def __init__(self, robo):
        self.robo = robo

    def girar(self, porta, sentido, rotacoes=1, potencia=75):
        return self.robo.motor_girar_rotacoes_porta(
            porta_ref=porta,
            sentido=sentido,
            rotacoes=rotacoes,
            potencia=potencia,
        )

    def arrancar(self, porta, sentido, potencia=75):
        return self.robo.motor_continuo_porta(
            porta_ref=porta,
            sentido=sentido,
            potencia=potencia,
        )

    def ir_posicao(self, porta, posicao, sentido, potencia=75):
        return self.robo.motor_ir_posicao_porta(
            porta_ref=porta,
            posicao=posicao,
            sentido=sentido,
            potencia=potencia,
        )

    def parar(self, porta):
        return self.robo.parar_motor_porta(porta)

    def posicao(self, porta):
        return self.robo.motor_posicao_porta(porta)

    def velocidade(self, porta):
        return self.robo.motor_velocidade_porta(porta)


class _AtuadorMovimentoFacade:
    def __init__(self, robo):
        self.robo = robo
        self.esq = None
        self.dir = None
        self.cm_por_rotacao = CIRCUNFERENCIA_PADRAO

    def configurar(self, esq, dir, cm_por_rotacao=17.5):
        self.esq = esq
        self.dir = dir
        self.cm_por_rotacao = float(cm_por_rotacao)
        return True

    def _garantir_configurado(self):
        if self.esq is None or self.dir is None:
            print("[Bot] ✗ Configure primeiro: robo.atuador.movimento.configurar(...)")
            return False
        return True

    def mover(self, sentido, cm=10, potencia=75):
        if not self._garantir_configurado():
            return False

        sentido_norm = str(sentido).lower()
        cm_assinado = abs(float(cm))
        if sentido_norm == "tras":
            cm_assinado = -cm_assinado
        elif sentido_norm != "frente":
            print("[Bot] ✗ Em mover(), sentido deve ser 'frente' ou 'tras'")
            return False

        rot = 0 if self.cm_por_rotacao == 0 else (cm_assinado / self.cm_por_rotacao)
        return (
            self.robo.motor_girar_rotacoes_porta(self.esq, sentido="horario", rotacoes=rot, potencia=potencia)
            and self.robo.motor_girar_rotacoes_porta(self.dir, sentido="horario", rotacoes=rot, potencia=potencia)
        )

    def arrancar(self, sentido, potencia=75):
        if not self._garantir_configurado():
            return False

        sentido_norm = str(sentido).lower()
        if sentido_norm == "frente":
            s_esq, s_dir = "horario", "horario"
        elif sentido_norm == "tras":
            s_esq, s_dir = "anti_horario", "anti_horario"
        elif sentido_norm == "direita":
            s_esq, s_dir = "horario", "anti_horario"
        elif sentido_norm == "esquerda":
            s_esq, s_dir = "anti_horario", "horario"
        else:
            print("[Bot] ✗ Sentido invalido. Use: frente, tras, direita, esquerda")
            return False

        return (
            self.robo.motor_continuo_porta(self.esq, sentido=s_esq, potencia=potencia)
            and self.robo.motor_continuo_porta(self.dir, sentido=s_dir, potencia=potencia)
        )

    def girar(self, sentido, graus=90, potencia=75):
        if not self._garantir_configurado():
            return False

        sentido_norm = str(sentido).lower()
        rot = abs(float(graus)) / 180.0
        if sentido_norm == "direita":
            return (
                self.robo.motor_girar_rotacoes_porta(self.esq, sentido="horario", rotacoes=rot, potencia=potencia)
                and self.robo.motor_girar_rotacoes_porta(self.dir, sentido="anti_horario", rotacoes=rot, potencia=potencia)
            )
        if sentido_norm == "esquerda":
            return (
                self.robo.motor_girar_rotacoes_porta(self.esq, sentido="anti_horario", rotacoes=rot, potencia=potencia)
                and self.robo.motor_girar_rotacoes_porta(self.dir, sentido="horario", rotacoes=rot, potencia=potencia)
            )

        print("[Bot] ✗ Em girar(), sentido deve ser 'direita' ou 'esquerda'")
        return False

    def parar(self):
        if not self._garantir_configurado():
            return False
        return self.robo.parar_motor_porta(self.esq) and self.robo.parar_motor_porta(self.dir)


class _AtuadorDisplayFacade:
    def __init__(self, robo):
        self.robo = robo

    def mostrar(self, texto):
        self.robo.mostrar_local(texto)


class _AtuadorLedFacade:
    def __init__(self, robo):
        self.robo = robo

    def cor(self, cor):
        self.robo.luz_local(cor)


class _AtuadorSomFacade:
    def __init__(self, robo):
        self.robo = robo

    def beep(self, frequencia=1000, duracao=200):
        self.robo.beep_local(frequencia, duracao)


class _AtuadorFacade:
    def __init__(self, robo):
        self.motor = _AtuadorMotorFacade(robo)
        self.movimento = _AtuadorMovimentoFacade(robo)
        self.display = _AtuadorDisplayFacade(robo)
        self.led = _AtuadorLedFacade(robo)
        self.som = _AtuadorSomFacade(robo)


class _SensorCorFacade:
    def __init__(self, robo):
        self.robo = robo

    def configurar(self, porta_ref, modo="reflexao"):
        return self.robo.hub_configurar_porta(porta_ref, "sensor_cor", modo=modo)

    def configurar_remoto(self, porta_ref, modo="reflexao"):
        return self.configurar(porta_ref, modo=modo)

    def ler(self, porta_ref):
        parsed = self.robo._parse_porta_remota(porta_ref)
        if not parsed:
            return "DESCONHECIDO"

        hub_alvo, porta_codigo = parsed
        if hub_alvo == self.robo.id_hub:
            nome = self.robo._garantir_sensor_local_por_codigo_porta(porta_codigo, "COR")
            if not nome:
                return "DESCONHECIDO"
            return self.robo.ler_cor_local(nome)

        return self.reflexao(porta_ref)

    def reflexao(self, porta_ref):
        parsed = self.robo._parse_porta_remota(porta_ref)
        if parsed:
            hub_alvo, porta_codigo = parsed
            if hub_alvo == self.robo.id_hub:
                nome = self.robo._garantir_sensor_local_por_codigo_porta(porta_codigo, "COR")
                if not nome:
                    return 0
                return self.robo.ler_reflexao_local(nome)

        return self.robo.ler_sensor_stream(porta_ref, BLESTREAM_TIPO_COR_REFLEXAO, default=0)

    def calibrar(self, porta_ref, nome_cor, segundos=5):
        parsed = self.robo._parse_porta_remota(porta_ref)
        if not parsed:
            return False

        hub_alvo, porta_codigo = parsed
        if hub_alvo != self.robo.id_hub:
            print("[Bot] ✗ Calibracao de cor so e suportada para sensor local")
            return False

        nome = self.robo._garantir_sensor_local_por_codigo_porta(porta_codigo, "COR")
        if not nome:
            return False
        self.robo.calibrar_cor_local(nome, nome_cor, tempo_s=segundos)
        return True


class _SensorDistanciaFacade:
    def __init__(self, robo):
        self.robo = robo

    def configurar(self, porta_ref):
        return self.robo.hub_configurar_porta(porta_ref, "sensor_ultra")

    def configurar_remoto(self, porta_ref):
        return self.configurar(porta_ref)

    def ler(self, porta_ref):
        parsed = self.robo._parse_porta_remota(porta_ref)
        if parsed:
            hub_alvo, porta_codigo = parsed
            if hub_alvo == self.robo.id_hub:
                nome = self.robo._garantir_sensor_local_por_codigo_porta(porta_codigo, "ULTRA")
                if not nome:
                    return 2000
                return self.robo.ler_distancia_local(nome)

        return self.robo.ler_sensor_stream(porta_ref, BLESTREAM_TIPO_DISTANCIA, default=2000)


class _SensorGiroscopioFacade:
    def __init__(self, robo):
        self.robo = robo

    def angulo(self):
        return self.robo.ler_angulo_local()

    def resetar(self):
        self.robo.resetar_giroscopio_local()


class _SensorFacade:
    def __init__(self, robo):
        self.cor = _SensorCorFacade(robo)
        self.distancia = _SensorDistanciaFacade(robo)
        self.giroscopio = _SensorGiroscopioFacade(robo)


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
        
        self._hub_hw = PrimeHub()
        self.nome_hub = self._hub_hw.system.name()
        
        # Detectar configuração BLE
        self._detectar_hub()

        # Fachada de hub com compatibilidade (hub físico + API de alto nível)
        self.hub = _HubFacade(self)
        
        # Periféricos locais
        self.motores_locais = {}
        self.sensores_locais = {}

        # Estado para protocolo BLE rapido
        self._blefast_seq = 0
        self._blefast_fila = []
        self._blefast_ultimo_estado = {}
        self._blefast_ultimo_seq_recebido = None

        # Estado do streaming de sensores
        self._blestream_seq = 0
        self._blestream_subs = {}
        self._blestream_buffer = {}
        self._blestream_ultimo_seq_por_hub = {}
        self._hub_portas_config = {}

        # Interface de alto nivel
        self.atuador = _AtuadorFacade(self)
        self.sensor = _SensorFacade(self)
        
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
        
        if "hub 1" in nome or "hub1" in nome or "spike0" in nome:
            self.canal_tx = CANAL_HUB1
            self.canais_rx = [CANAL_HUB2, CANAL_HUB3]
            self.modo_ble = "servidor"
            self.id_hub = 1
        elif "hub 2" in nome or "hub2" in nome or "spike1" in nome:
            self.canal_tx = CANAL_HUB2
            self.canais_rx = [CANAL_HUB1, CANAL_HUB3]
            self.modo_ble = "cliente"
            self.id_hub = 2
        elif "hub 3" in nome or "hub3" in nome or "spike2" in nome:
            self.canal_tx = CANAL_HUB3
            self.canais_rx = [CANAL_HUB1, CANAL_HUB2]
            self.modo_ble = "cliente"
            self.id_hub = 3
        else:
            self.canal_tx = CANAL_HUB3
            self.canais_rx = [CANAL_HUB1, CANAL_HUB2]
            self.modo_ble = "cliente"
            self.id_hub = 3
        
        # Tentar inicializar BLE
        try:
            self._hub_hw = PrimeHub(
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

    def configurar_hardware_local_automatico(self, portas=None):
        """Detecta automaticamente motores e sensores nas portas locais.

        Use no Hub multiplexador para não precisar configurar portas manualmente.
        """
        if portas is None:
            portas = (Port.A, Port.B, Port.C, Port.D, Port.E, Port.F)

        letras = {
            Port.A: "A",
            Port.B: "B",
            Port.C: "C",
            Port.D: "D",
            Port.E: "E",
            Port.F: "F",
        }

        novos_motores = 0
        novos_cor = 0
        novos_ultra = 0

        for porta in portas:
            letra = letras.get(porta, "?")

            # Evita duplicar se já existe motor nessa porta.
            ja_tem_motor = False
            for info in self.motores_locais.values():
                if info.get("porta") == porta:
                    ja_tem_motor = True
                    break

            if not ja_tem_motor:
                try:
                    motor = Motor(porta)
                    nome_motor = f"motor_{letra}"
                    self.motores_locais[nome_motor] = {
                        "motor": motor,
                        "nome": nome_motor,
                        "porta": porta,
                    }
                    novos_motores += 1
                    print(f"[Bot] ✓ Auto motor '{nome_motor}' em Port.{letra}")
                except:
                    pass

            # Evita duplicar sensores já registrados nessa porta.
            ja_tem_cor = False
            ja_tem_ultra = False
            for info in self.sensores_locais.values():
                if info.get("porta") != porta:
                    continue
                if info.get("tipo") == "COR":
                    ja_tem_cor = True
                if info.get("tipo") == "ULTRA":
                    ja_tem_ultra = True

            if not ja_tem_cor:
                try:
                    sensor_cor = ColorSensor(porta)
                    nome_cor = f"cor_{letra}"
                    self.sensores_locais[nome_cor] = {
                        "sensor": sensor_cor,
                        "tipo": "COR",
                        "porta": porta,
                    }
                    novos_cor += 1
                    print(f"[Bot] ✓ Auto sensor cor '{nome_cor}' em Port.{letra}")
                except:
                    pass

            if not ja_tem_ultra:
                try:
                    sensor_ultra = UltrasonicSensor(porta)
                    nome_ultra = f"ultra_{letra}"
                    self.sensores_locais[nome_ultra] = {
                        "sensor": sensor_ultra,
                        "tipo": "ULTRA",
                        "porta": porta,
                    }
                    novos_ultra += 1
                    print(f"[Bot] ✓ Auto sensor ultra '{nome_ultra}' em Port.{letra}")
                except:
                    pass

        print(
            f"[Bot] Auto-config: {novos_motores} motores, {novos_cor} cor, {novos_ultra} ultra"
        )
        return {
            "motores": novos_motores,
            "cor": novos_cor,
            "ultra": novos_ultra,
        }
    
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

    def _porta_letra_para_codigo(self, letra):
        mapa = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
        return mapa.get(str(letra).upper(), 0)

    def _porta_codigo_para_obj(self, codigo):
        mapa = {
            1: Port.A,
            2: Port.B,
            3: Port.C,
            4: Port.D,
            5: Port.E,
            6: Port.F,
        }
        return mapa.get(codigo)

    def _parse_porta_remota(self, porta_ref):
        """Converte entrada em (hub_alvo, codigo_porta)."""
        if porta_ref == Port.A:
            return (self.id_hub, 1)
        if porta_ref == Port.B:
            return (self.id_hub, 2)
        if porta_ref == Port.C:
            return (self.id_hub, 3)
        if porta_ref == Port.D:
            return (self.id_hub, 4)
        if porta_ref == Port.E:
            return (self.id_hub, 5)
        if porta_ref == Port.F:
            return (self.id_hub, 6)

        if isinstance(porta_ref, str):
            texto = porta_ref.strip().upper()
            if texto.startswith("PORT."):
                texto = texto[5:]

            if len(texto) == 1:
                porta_codigo = self._porta_letra_para_codigo(texto)
                if porta_codigo == 0:
                    return None
                return (self.id_hub, porta_codigo)

            if len(texto) < 2:
                return None

            letra = texto[0]
            try:
                hub_alvo = int(texto[1:])
            except:
                return None
            porta_codigo = self._porta_letra_para_codigo(letra)
            if porta_codigo == 0 or hub_alvo < 1:
                return None
            return (hub_alvo, porta_codigo)

        if isinstance(porta_ref, tuple) and len(porta_ref) == 2:
            return (int(porta_ref[0]), int(porta_ref[1]))

        return None

    def _porta_obj_para_codigo(self, porta_obj):
        if porta_obj == Port.A:
            return 1
        if porta_obj == Port.B:
            return 2
        if porta_obj == Port.C:
            return 3
        if porta_obj == Port.D:
            return 4
        if porta_obj == Port.E:
            return 5
        if porta_obj == Port.F:
            return 6
        return 0

    def _nome_motor_por_codigo_porta(self, codigo_porta):
        porta_obj = self._porta_codigo_para_obj(codigo_porta)
        if porta_obj is None:
            return None

        for nome, info in self.motores_locais.items():
            if info.get("porta") == porta_obj:
                return nome
        return None

    def _garantir_motor_local_por_codigo_porta(self, codigo_porta):
        """Retorna nome do motor da porta; cria registro automático se necessário."""
        nome_motor = self._nome_motor_por_codigo_porta(codigo_porta)
        if nome_motor:
            return nome_motor

        porta_obj = self._porta_codigo_para_obj(codigo_porta)
        if porta_obj is None:
            return None

        nome_auto = f"motor_p{codigo_porta}"
        if self.adicionar_motor_local(nome_auto, porta_obj):
            return nome_auto
        return None

    def _nome_sensor_por_codigo_porta_tipo(self, codigo_porta, tipo_local):
        porta_obj = self._porta_codigo_para_obj(codigo_porta)
        if porta_obj is None:
            return None

        for nome, info in self.sensores_locais.items():
            if info.get("porta") == porta_obj and info.get("tipo") == str(tipo_local):
                return nome
        return None

    def _garantir_sensor_local_por_codigo_porta(self, codigo_porta, tipo_local):
        nome = self._nome_sensor_por_codigo_porta_tipo(codigo_porta, tipo_local)
        if nome:
            return nome

        porta_obj = self._porta_codigo_para_obj(codigo_porta)
        if porta_obj is None:
            return None

        tipo_local = str(tipo_local)
        if tipo_local == "COR":
            nome_auto = f"cor_p{codigo_porta}"
            if self.adicionar_sensor_cor_local(nome_auto, porta_obj):
                return nome_auto

        if tipo_local == "ULTRA":
            nome_auto = f"ultra_p{codigo_porta}"
            if self.adicionar_sensor_ultra_local(nome_auto, porta_obj):
                return nome_auto

        return None

    def _sentido_motor_para_sinal(self, sentido):
        s = str(sentido).strip().lower()
        if s in ("horario", "frente", "clockwise"):
            return 1
        if s in ("anti_horario", "antihorario", "tras", "counterclockwise"):
            return -1
        return 0

    def motor_girar_rotacoes_porta(self, porta_ref, sentido, rotacoes=1, potencia=75):
        sinal = self._sentido_motor_para_sinal(sentido)
        if sinal == 0:
            print("[Bot] ✗ Sentido invalido. Use 'horario' ou 'anti_horario'")
            return False

        graus = int(abs(float(rotacoes)) * 360)
        if sinal < 0:
            graus = -graus
        return self.motor_graus_porta(porta_ref, graus=graus, potencia=potencia)

    def motor_continuo_porta(self, porta_ref, sentido, potencia=75):
        parsed = self._parse_porta_remota(porta_ref)
        if not parsed:
            print("[Bot] ✗ Porta invalida. Use Port.A, 'A1', 'B2', etc.")
            return False

        hub_alvo, porta_codigo = parsed
        sinal = self._sentido_motor_para_sinal(sentido)
        if sinal == 0:
            print("[Bot] ✗ Sentido invalido. Use 'horario' ou 'anti_horario'")
            return False

        if hub_alvo == self.id_hub:
            nome_motor = self._garantir_motor_local_por_codigo_porta(porta_codigo)
            if not nome_motor:
                return False

            vel = max(100, int(potencia) * 10)
            if sinal < 0:
                vel = -vel
            self.motor_local_continuo(nome_motor, vel)
            return True

        sentido_ble = BLEFAST_SENTIDO_FRENTE if sinal > 0 else BLEFAST_SENTIDO_TRAS
        self.enfileirar_comando_remoto(
            hub_alvo,
            porta_codigo,
            BLEFAST_CMD_CONTINUO,
            sentido=sentido_ble,
            valor=0,
            potencia=potencia,
            forcar=True,
        )
        return self.enviar_lote_remoto(hub_alvo, max_comandos=3)

    def parar_motor_porta(self, porta_ref):
        parsed = self._parse_porta_remota(porta_ref)
        if not parsed:
            return False

        hub_alvo, porta_codigo = parsed
        if hub_alvo == self.id_hub:
            nome_motor = self._nome_motor_por_codigo_porta(porta_codigo)
            if not nome_motor:
                return False
            self.parar_motor_local(nome_motor)
            return True

        self.enfileirar_comando_remoto(
            hub_alvo,
            porta_codigo,
            BLEFAST_CMD_PARAR,
            sentido=BLEFAST_SENTIDO_FRENTE,
            valor=0,
            potencia=0,
            forcar=True,
        )
        return self.enviar_lote_remoto(hub_alvo, max_comandos=3)

    def motor_ir_posicao_porta(self, porta_ref, posicao=0, sentido="curto", potencia=75):
        parsed = self._parse_porta_remota(porta_ref)
        if not parsed:
            print("[Bot] ✗ Porta invalida")
            return False

        hub_alvo, porta_codigo = parsed
        alvo = int(posicao)
        vel = max(100, int(potencia) * 10)
        sentido_norm = str(sentido).strip().lower()

        if hub_alvo == self.id_hub:
            nome_motor = self._garantir_motor_local_por_codigo_porta(porta_codigo)
            if not nome_motor:
                return False

            motor = self.motores_locais[nome_motor]["motor"]
            if sentido_norm == "curto":
                motor.run_target(vel, alvo)
                return True

            atual = int(motor.angle())
            if sentido_norm in ("horario", "clockwise"):
                alvo_ajustado = alvo
                while alvo_ajustado < atual:
                    alvo_ajustado += 360
                motor.run_target(vel, alvo_ajustado)
                return True

            if sentido_norm in ("anti_horario", "antihorario", "counterclockwise"):
                alvo_ajustado = alvo
                while alvo_ajustado > atual:
                    alvo_ajustado -= 360
                motor.run_target(vel, alvo_ajustado)
                return True

            print("[Bot] ✗ Sentido invalido. Use: curto, horario, anti_horario")
            return False

        # Em remoto, sem telemetria de posicao absoluta, usa deslocamento relativo.
        if sentido_norm in ("anti_horario", "antihorario", "counterclockwise"):
            alvo = -abs(alvo)
        else:
            alvo = abs(alvo)
        return self.motor_graus_porta(porta_ref, graus=alvo, potencia=potencia)

    def motor_posicao_porta(self, porta_ref):
        parsed = self._parse_porta_remota(porta_ref)
        if not parsed:
            return 0

        hub_alvo, porta_codigo = parsed
        if hub_alvo != self.id_hub:
            print("[Bot] ✗ Leitura de posicao remota nao suportada nesta versao")
            return 0

        nome_motor = self._garantir_motor_local_por_codigo_porta(porta_codigo)
        if not nome_motor:
            return 0
        return int(self.motores_locais[nome_motor]["motor"].angle())

    def motor_velocidade_porta(self, porta_ref):
        parsed = self._parse_porta_remota(porta_ref)
        if not parsed:
            return 0

        hub_alvo, porta_codigo = parsed
        if hub_alvo != self.id_hub:
            print("[Bot] ✗ Leitura de velocidade remota nao suportada nesta versao")
            return 0

        nome_motor = self._garantir_motor_local_por_codigo_porta(porta_codigo)
        if not nome_motor:
            return 0
        return int(self.motores_locais[nome_motor]["motor"].speed())

    def _blefast_checksum(self, dados):
        chk = 0
        for b in dados:
            chk ^= (b & 0xFF)
        return chk & 0xFF

    def _normalizar_tipo_porta_remota(self, tipo):
        t = str(tipo).strip().lower()
        t = t.replace(" ", "_").replace("-", "_")

        if t in ("sensor_cor", "sensor_de_cor", "cor", "color"):
            return "sensor_cor"
        if t in (
            "sensor_ultra",
            "sensor_ultrassonico",
            "sensor_ultrasonico",
            "ultra",
            "ultrassonico",
            "ultrasonico",
            "distancia",
        ):
            return "sensor_ultra"
        if t in ("motor", "atuador"):
            return "motor"
        return None

    def hub_configurar_porta(self, porta_ref, tipo, modo=""):
        """Configura no Hub 1 o tipo de dispositivo esperado em uma porta remota.

        Ex:
            robo.hub_configurar_porta("A2", "sensor_cor")
            robo.hub_configurar_porta("B2", "sensor_cor")
            robo.hub_configurar_porta("C2", "motor")
        """
        parsed = self._parse_porta_remota(porta_ref)
        if not parsed:
            print("[Bot] ✗ Porta invalida. Use formato 'A2', 'B2', 'C2', etc.")
            return False

        tipo_norm = self._normalizar_tipo_porta_remota(tipo)
        if tipo_norm is None:
            print("[Bot] ✗ Tipo invalido. Use: sensor_cor, sensor_ultra ou motor")
            return False

        hub_alvo, porta_codigo = parsed
        chave = (hub_alvo, porta_codigo)

        if tipo_norm == "sensor_cor":
            modo_final = modo if modo else "reflexao"
            ok = self.configurar_sensor_remoto_stream(
                porta_ref,
                tipo=BLESTREAM_TIPO_COR_REFLEXAO,
                modo=modo_final,
            )
            if not ok:
                return False
            self._hub_portas_config[chave] = {"tipo": "sensor_cor", "modo": modo_final}
            print(f"[Bot] ✓ Porta {porta_ref} configurada como sensor de cor ({modo_final})")
            return True

        if tipo_norm == "sensor_ultra":
            ok = self.configurar_sensor_remoto_stream(
                porta_ref,
                tipo=BLESTREAM_TIPO_DISTANCIA,
                modo="distancia",
            )
            if not ok:
                return False
            self._hub_portas_config[chave] = {"tipo": "sensor_ultra", "modo": "distancia"}
            print(f"[Bot] ✓ Porta {porta_ref} configurada como sensor ultrassonico")
            return True

        self._hub_portas_config[chave] = {"tipo": "motor", "modo": ""}
        print(f"[Bot] ✓ Porta {porta_ref} configurada como motor remoto")
        return True

    def hub_configurar_portas(self, configuracoes):
        """Configura varias portas remotas em lote.

        Formatos aceitos por item da lista:
            ("A2", "sensor_cor")
            ("A2", "sensor_cor", "reflexao")
        """
        ok_total = True
        for item in configuracoes:
            if not isinstance(item, tuple):
                ok_total = False
                continue

            if len(item) == 2:
                porta_ref, tipo = item
                modo = ""
            elif len(item) == 3:
                porta_ref, tipo, modo = item
            else:
                ok_total = False
                continue

            if not self.hub_configurar_porta(porta_ref, tipo, modo=modo):
                ok_total = False

        return ok_total

    def configurar_sensor_remoto_stream(self, porta_ref, tipo, modo=""):
        parsed = self._parse_porta_remota(porta_ref)
        if not parsed:
            print("[Bot] ✗ Porta de sensor invalida. Use 'D2', 'C2', etc.")
            return False

        hub_alvo, porta_codigo = parsed
        self._blestream_subs[(hub_alvo, porta_codigo, int(tipo))] = {
            "modo": str(modo),
        }
        return True

    def _ler_sensor_local_por_porta_tipo(self, porta_codigo, tipo):
        porta_obj = self._porta_codigo_para_obj(porta_codigo)
        if porta_obj is None:
            return None

        for _, info in self.sensores_locais.items():
            if info.get("porta") != porta_obj:
                continue

            sensor = info.get("sensor")
            tipo_local = info.get("tipo")

            if tipo == BLESTREAM_TIPO_COR_REFLEXAO and tipo_local == "COR":
                try:
                    return sensor.reflection()
                except:
                    return 0

            if tipo == BLESTREAM_TIPO_DISTANCIA and tipo_local == "ULTRA":
                try:
                    return sensor.distance()
                except:
                    return 2000

        return None

    def transmitir_stream_sensores_local(self):
        """Hub remoto: lê sensores locais e transmite continuamente em pacote binário."""
        entradas = []

        for _, info in self.sensores_locais.items():
            porta_obj = info.get("porta")
            porta_codigo = self._porta_obj_para_codigo(porta_obj)
            if porta_codigo == 0:
                continue

            tipo_local = info.get("tipo")
            sensor = info.get("sensor")

            if tipo_local == "COR":
                try:
                    valor = int(sensor.reflection())
                except:
                    valor = 0
                valor = max(0, min(65535, valor))
                entradas.append((porta_codigo, BLESTREAM_TIPO_COR_REFLEXAO, valor))

            elif tipo_local == "ULTRA":
                try:
                    valor = int(sensor.distance())
                except:
                    valor = 2000
                valor = max(0, min(65535, valor))
                entradas.append((porta_codigo, BLESTREAM_TIPO_DISTANCIA, valor))

        if not entradas:
            return False

        # Até 5 entradas para manter pacote < 27 bytes.
        entradas = entradas[:5]

        self._blestream_seq = (self._blestream_seq + 1) & 0xFF
        if self._blestream_seq == 0:
            self._blestream_seq = 1

        dados = [BLESTREAM_MAGIC, self._blestream_seq, self.id_hub, len(entradas)]
        for porta_codigo, tipo, valor in entradas:
            dados.extend([
                porta_codigo,
                tipo,
                (valor >> 8) & 0xFF,
                valor & 0xFF,
            ])

        dados.append(self._blefast_checksum(dados))
        pacote = bytes(dados)

        try:
            self.hub.ble.broadcast(data=pacote)
            return True
        except:
            return False

    def atualizar_stream_sensores(self):
        """Hub consumidor: processa último pacote de streaming e atualiza buffer local."""
        msg = self.receber_ble()
        if not isinstance(msg, (bytes, bytearray)):
            return False

        if len(msg) < 5 or msg[0] != BLESTREAM_MAGIC:
            return False

        if self._blefast_checksum(msg[:-1]) != msg[-1]:
            return False

        seq = msg[1]
        hub_src = msg[2]
        qtd = msg[3]

        tamanho_esperado = 5 + (qtd * 4)
        if len(msg) != tamanho_esperado:
            return False

        if self._blestream_ultimo_seq_por_hub.get(hub_src) == seq:
            return False

        i = 4
        for _ in range(qtd):
            porta_codigo = msg[i]
            tipo = msg[i + 1]
            valor = (msg[i + 2] << 8) | msg[i + 3]
            self._blestream_buffer[(hub_src, porta_codigo, tipo)] = valor
            i += 4

        self._blestream_ultimo_seq_por_hub[hub_src] = seq
        return True

    def ler_sensor_stream(self, porta_ref, tipo, default=0):
        """Lê sensor local/remoto via API unificada com buffer de streaming."""
        parsed = self._parse_porta_remota(porta_ref)
        if not parsed:
            print("[Bot] ✗ Porta de sensor invalida. Use 'D1', 'D2', etc.")
            return default

        hub_alvo, porta_codigo = parsed
        tipo = int(tipo)

        if hub_alvo == self.id_hub:
            valor_local = self._ler_sensor_local_por_porta_tipo(porta_codigo, tipo)
            if valor_local is None:
                return default
            return valor_local

        # Atualiza buffer rapidamente com o último pacote disponível.
        self.atualizar_stream_sensores()
        return self._blestream_buffer.get((hub_alvo, porta_codigo, tipo), default)

    def enfileirar_comando_remoto(self, hub_alvo, porta_codigo, comando, sentido=1, valor=0, potencia=75, forcar=False):
        """Enfileira comando remoto com delta e prioridade de parada."""
        hub_alvo = int(hub_alvo)
        porta_codigo = int(porta_codigo)
        comando = int(comando)
        sentido = int(sentido)
        valor = int(abs(valor))
        potencia = int(potencia)

        valor = max(0, min(65535, valor))
        potencia = max(0, min(100, potencia))

        chave = (hub_alvo, porta_codigo, comando)
        estado = (sentido, valor, potencia)

        if not forcar and self._blefast_ultimo_estado.get(chave) == estado:
            return False

        prioridade = 0 if comando == BLEFAST_CMD_PARAR else 1
        self._blefast_fila.append({
            "hub": hub_alvo,
            "porta": porta_codigo,
            "cmd": comando,
            "sentido": sentido,
            "valor": valor,
            "pot": potencia,
            "prio": prioridade,
        })
        self._blefast_ultimo_estado[chave] = estado
        return True

    def enviar_lote_remoto(self, hub_alvo=None, max_comandos=3):
        """Monta e envia lote binário rapido (até 3 comandos)."""
        if not self._blefast_fila:
            return False

        max_comandos = max(1, min(3, int(max_comandos)))
        if hub_alvo is None:
            hub_alvo = self._blefast_fila[0]["hub"]

        candidatos = []
        for idx, item in enumerate(self._blefast_fila):
            if item["hub"] == hub_alvo:
                candidatos.append((idx, item))

        if not candidatos:
            return False

        candidatos.sort(key=lambda x: x[1]["prio"])
        selecionados = candidatos[:max_comandos]

        # Remove da fila de trás para frente para manter índices válidos.
        for idx, _ in sorted(selecionados, key=lambda x: x[0], reverse=True):
            self._blefast_fila.pop(idx)

        self._blefast_seq = (self._blefast_seq + 1) & 0xFF
        if self._blefast_seq == 0:
            self._blefast_seq = 1

        dados = [BLEFAST_MAGIC, self._blefast_seq, int(hub_alvo), len(selecionados)]
        for _, item in selecionados:
            valor = item["valor"]
            dados.extend([
                item["porta"],
                item["cmd"],
                item["sentido"],
                (valor >> 8) & 0xFF,
                valor & 0xFF,
                item["pot"],
            ])

        dados.append(self._blefast_checksum(dados))
        pacote = bytes(dados)

        try:
            self.hub.ble.broadcast(data=pacote)
            return True
        except Exception as e:
            print(f"[Bot] Erro BLE rápido: {e}")
            return False

    def receber_ble_rapido(self):
        """Recebe e decodifica pacote binário rápido."""
        msg = self.receber_ble()
        if msg is None:
            return None

        if not isinstance(msg, (bytes, bytearray)):
            return None

        if len(msg) < 5:
            return None

        if msg[0] != BLEFAST_MAGIC:
            return None

        if self._blefast_checksum(msg[:-1]) != msg[-1]:
            return None

        seq = msg[1]
        hub_alvo = msg[2]
        qtd = msg[3]

        if hub_alvo != self.id_hub:
            return None

        if self._blefast_ultimo_seq_recebido == seq:
            return None

        tamanho_esperado = 5 + (qtd * 6)
        if len(msg) != tamanho_esperado:
            return None

        comandos = []
        i = 4
        for _ in range(qtd):
            porta = msg[i]
            cmd = msg[i + 1]
            sentido = msg[i + 2]
            valor = (msg[i + 3] << 8) | msg[i + 4]
            pot = msg[i + 5]
            comandos.append((porta, cmd, sentido, valor, pot))
            i += 6

        self._blefast_ultimo_seq_recebido = seq
        return {
            "seq": seq,
            "hub": hub_alvo,
            "comandos": comandos,
        }

    def executar_ble_rapido(self, pacote):
        """Executa comandos rápidos recebidos via BLE."""
        if not pacote:
            return False

        for porta_codigo, cmd, sentido, valor, pot in pacote["comandos"]:
            nome_motor = self._nome_motor_por_codigo_porta(porta_codigo)
            if not nome_motor:
                continue

            if cmd == BLEFAST_CMD_PARAR:
                self.parar_motor_local(nome_motor)

            elif cmd == BLEFAST_CMD_CONTINUO:
                vel = max(100, int(pot) * 10)
                if sentido == BLEFAST_SENTIDO_TRAS:
                    vel = -vel
                self.motor_local_continuo(nome_motor, vel)

            elif cmd == BLEFAST_CMD_GRAUS:
                graus = int(valor)
                if sentido == BLEFAST_SENTIDO_TRAS:
                    graus = -graus
                vel = max(100, int(pot) * 10)
                self.motor_local_graus(nome_motor, graus, vel)

            elif cmd == BLEFAST_CMD_CM:
                cm = int(valor)
                if sentido == BLEFAST_SENTIDO_TRAS:
                    cm = -cm
                vel = max(100, int(pot) * 10)
                self.motor_local_cm(nome_motor, cm, velocidade=vel)

        return True

    def enviar_motor_graus_remoto(self, porta_remota, graus=360, potencia=75):
        """Atalho para enviar um comando de giro remoto em pacote rapido."""
        parsed = self._parse_porta_remota(porta_remota)
        if not parsed:
            print("[Bot] ✗ Porta remota invalida. Use formato 'A2', 'B3', etc.")
            return False

        hub_alvo, porta_codigo = parsed
        sentido = BLEFAST_SENTIDO_FRENTE
        if int(graus) < 0:
            sentido = BLEFAST_SENTIDO_TRAS

        self.enfileirar_comando_remoto(
            hub_alvo,
            porta_codigo,
            BLEFAST_CMD_GRAUS,
            sentido=sentido,
            valor=abs(int(graus)),
            potencia=potencia,
            forcar=True,
        )
        return self.enviar_lote_remoto(hub_alvo, max_comandos=3)

    def motor_graus_porta(self, porta_ref, graus=360, potencia=75):
        """Controle unificado por porta: A1 local, A2 remoto, A3 remoto..."""
        parsed = self._parse_porta_remota(porta_ref)
        if not parsed:
            print("[Bot] ✗ Porta invalida. Use formato 'A1', 'B2', 'C3', etc.")
            return False

        hub_alvo, porta_codigo = parsed

        # Mesmo hub: executa localmente por porta
        if hub_alvo == self.id_hub:
            nome_motor = self._garantir_motor_local_por_codigo_porta(porta_codigo)
            if not nome_motor:
                print("[Bot] ✗ Não foi possível usar a porta local")
                return False

            velocidade = max(100, int(potencia) * 10)
            self.motor_local_graus(nome_motor, graus, velocidade)
            return True

        # Outro hub: envia pelo protocolo rápido
        return self.enviar_motor_graus_remoto(porta_ref, graus=graus, potencia=potencia)

    def motor_girar(self, porta_ref, horario=True, graus=360, potencia=75):
        """API principal unificada: A1 local, A2 remoto, A3 remoto.

        Ex:
            robo.motor_girar("B2", horario=True, graus=360, potencia=90)
        """
        sentido_horario = bool(horario)
        graus_assinados = abs(int(graus)) if sentido_horario else -abs(int(graus))
        return self.motor_graus_porta(porta_ref, graus=graus_assinados, potencia=potencia)

    # ==========================================
    # API UNIFICADA (SEM SUFIXO)
    # ==========================================

    def mostrar(self, texto):
        return self.mostrar_local(texto)

    def limpar_display(self):
        return self.limpar_display_local()

    def botao_pressionado(self):
        return bool(self.botao_pressionado_local())

    def esperar_botao(self, timeout_ms=10000):
        return self.esperar_botao_local(timeout_ms=timeout_ms)

    def configurar_hardware_automatico(self, portas=None):
        return self.configurar_hardware_local_automatico(portas=portas)

    def transmitir_stream_sensores(self):
        return self.transmitir_stream_sensores_local()
    
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
            for canal in self.canais_rx:
                msg = self.hub.ble.observe(canal)
                if msg is not None:
                    return msg
            return None
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
