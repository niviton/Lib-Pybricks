# 📚 Biblioteca CNATMake_lib

Biblioteca unificada para controle de robôs SPIKE Prime com PyBricks.

## 📦 Conteúdo

- `CNATMake_lib.py` - Classe principal com todas as funcionalidades

## 🚀 Uso

```python
from lib.CNATMake_lib import CNATMake_lib
from pybricks.parameters import Port

# Criar instância
bot = CNATMake_lib()

# Adicionar periféricos
bot.adicionar_motor("roda", Port.A)
bot.adicionar_sensor_cor("cor", Port.D)

# Usar
bot.motor("roda").mover_cm(20)
cor = bot.sensor("cor").ler_cor()
```

## 📖 Documentação Completa

Veja [GUIA_CNATMake_lib.md](../GUIA_CNATMake_lib.md) na raiz do projeto.
