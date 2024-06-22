# logging_setup.py
import logging


# Configuração básica
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(
    filename="app.log",
    level=logging.DEBUG,  # Certifique-se de que o nível de logging seja DEBUG para capturar todas as mensagens
    format=LOG_FORMAT,
    filemode='w'
)

# Configura o logger principal
logger = logging.getLogger()

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(console_handler)


