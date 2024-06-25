import logging
from logging.handlers import RotatingFileHandler
# Configuração básica
LOG_FORMAT = "%(levelname)s | %(asctime)s - %(message)s"
LOG_FILENAME = "app.log"
LOG_LEVEL = logging.INFO
LOG_NAME = "PHUTBEND"

logging.basicConfig(
    filename=LOG_FILENAME,
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    filemode='w'
)

# Configura o logger principal
logger = logging.getLogger()

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(console_handler)
handler = RotatingFileHandler(LOG_FILENAME, maxBytes=2000, backupCount=5)