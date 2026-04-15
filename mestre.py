# ============================================================
#  MESTRE — Hub que envia comandos e espera respostas
#  Carregue este arquivo no hub "mestre" (ex.: SPIKE Prime)
# ============================================================

from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Color
from pybricks.tools import wait

# ── Canais BLE ──────────────────────────────────────────────
CANAL_MESTRE = 1   # canal em que este hub transmite
CANAL_SERVO  = 2   # canal em que o servo transmite (mestre escuta)

# ── Comandos (mestre → servo) ────────────────────────────────
CMD_PING      = 0
CMD_LIGAR_LED = 1
CMD_APAGAR_LED= 2
# Adicione mais comandos conforme necessário

# ── Respostas (servo → mestre) ───────────────────────────────
RSP_PONG      = 0
RSP_LED_LIGADO= 1
RSP_LED_APAGADO=2

# ── Inicialização ────────────────────────────────────────────
hub = PrimeHub(
    broadcast_channel=CANAL_MESTRE,
    observe_channels=[CANAL_SERVO],
)
hub.system.set_stop_button(Button.CENTER)


# ── Funções de comunicação ───────────────────────────────────

def enviar_comando(*args):
    """Envia uma tupla de valores via BLE broadcast."""
    hub.ble.broadcast(tuple(args))


def esperar_resposta(esperado):
    """
    Fica em loop até receber do servo a resposta esperada.
    Retorna os argumentos extras que vierem junto com a resposta.
    """
    while True:
        try:
            dados = hub.ble.observe(CANAL_SERVO)
            if dados is None:
                continue
            codigo, *extras = dados
            if codigo == esperado:
                return extras[0] if len(extras) == 1 else extras
        except (RuntimeError, UnicodeError):
            continue


# ── Ações de alto nível ──────────────────────────────────────

def ping():
    print("Enviando PING...")
    enviar_comando(CMD_PING)
    esperar_resposta(RSP_PONG)
    print("Recebeu PONG!")


def ligar_led():
    print("Ligando LED do servo...")
    enviar_comando(CMD_LIGAR_LED)
    esperar_resposta(RSP_LED_LIGADO)
    print("LED ligado!")


def apagar_led():
    print("Apagando LED do servo...")
    enviar_comando(CMD_APAGAR_LED)
    esperar_resposta(RSP_LED_APAGADO)
    print("LED apagado!")


# ── Loop principal ───────────────────────────────────────────

hub.light.on(Color.GREEN)
print("Mestre pronto.")

while True:
    botoes = hub.buttons.pressed()

    if Button.LEFT in botoes:
        ligar_led()
        wait(300)

    elif Button.RIGHT in botoes:
        apagar_led()
        wait(300)

    elif Button.BLUETOOTH in botoes:
        ping()
        wait(300)

    wait(50)
