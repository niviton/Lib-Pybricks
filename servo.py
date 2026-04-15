# ============================================================
#  SERVO — Hub que recebe comandos e envia respostas
#  Carregue este arquivo no hub "servo" (ex.: SPIKE Prime)
# ============================================================

from pybricks.hubs import PrimeHub
from pybricks.parameters import Button, Color
from pybricks.tools import wait

# ── Canais BLE ──────────────────────────────────────────────
CANAL_MESTRE = 1   # canal em que o mestre transmite (servo escuta)
CANAL_SERVO  = 2   # canal em que este hub transmite

# ── Comandos (mestre → servo) ────────────────────────────────
CMD_PING      = 0
CMD_LIGAR_LED = 1
CMD_APAGAR_LED= 2

# ── Respostas (servo → mestre) ───────────────────────────────
RSP_PONG      = 0
RSP_LED_LIGADO= 1
RSP_LED_APAGADO=2

# ── Inicialização ────────────────────────────────────────────
hub = PrimeHub(
    broadcast_channel=CANAL_SERVO,
    observe_channels=[CANAL_MESTRE],
)
hub.system.set_stop_button(Button.CENTER)


# ── Funções de comunicação ───────────────────────────────────

def enviar_resposta(*args):
    """Envia uma tupla de valores via BLE broadcast."""
    hub.ble.broadcast(tuple(args))


# ── Loop principal — aguarda e executa comandos ──────────────

hub.light.on(Color.CYAN)
print("Servo pronto, aguardando comandos...")

cmd_anterior = None

while True:
    try:
        dados = hub.ble.observe(CANAL_MESTRE)
    except (RuntimeError, UnicodeError):
        continue

    if dados is None:
        continue

    # Só processa quando recebe um novo comando
    # (evita executar o mesmo comando em loop)
    if dados == cmd_anterior:
        wait(10)
        continue

    cmd_anterior = dados
    codigo, *args = dados
    print("Comando recebido:", codigo, args)

    # ── Tratamento de cada comando ───────────────────────────

    if codigo == CMD_PING:
        print("PING recebido, enviando PONG")
        enviar_resposta(RSP_PONG)

    elif codigo == CMD_LIGAR_LED:
        hub.light.on(Color.YELLOW)
        print("LED ligado")
        enviar_resposta(RSP_LED_LIGADO)

    elif codigo == CMD_APAGAR_LED:
        hub.light.off()
        print("LED apagado")
        enviar_resposta(RSP_LED_APAGADO)

    # Adicione mais elif aqui para novos comandos

    wait(10)
