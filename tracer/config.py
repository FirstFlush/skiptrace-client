import logging
import os
from termcolor import colored
import logging.config
import json

with open('tracer/config.json', 'r') as f:
    json_settings = json.load(f)



# ENDPOINTS
# ============================================
DOMAIN = json_settings['SERVER']['domain']
LAUNCH_URL = json_settings['SERVER']['endpoints']['launch']
LIST_URL = json_settings['SERVER']['endpoints']['list']


# Debug Status
# ============================================
DEBUG = False
if DEBUG is True:
    LOG_LEVEL = "DEBUG"
else:
    LOG_LEVEL = "INFO"

# Constants
# ============================================
LOG_DIR = os.path.join(os.path.dirname(__file__), 'log')


# Logging
# ============================================
class ColoredFormatter(logging.Formatter):

    COLORS = {
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red',
        'DEBUG': 'blue',
        'INFO': 'green'
    }

    def format(self, record):
        log_message = super().format(record)
        color = self.COLORS.get(record.levelname, 'white')
        colored_levelname = colored(record.levelname, color)
        return log_message.replace(record.levelname, colored_levelname)

    # def bold(msg:str):
    #     return f"\033[1m{msg}\033[0m"


LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(levelname)s - %(message)s",
        },
        "colored": {
            "()": ColoredFormatter,  # replace with your actual module path
            "format": "%(levelname)-10s%(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "colored",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": os.path.join(LOG_DIR, "client.log"),
            "level": "WARNING",
            "formatter": "default",
        },
    },
    "loggers": {
        "client": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)
client_logger = logging.getLogger('client')


# client_logger = logging.getLogger('client')

# if DEBUG == True:
#     client_logger.setLevel(logging.DEBUG)
# else:
#     client_logger.setLevel(logging.INFO)

# log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# stream_formatter = ColoredFormatter('%(levelname)-10s%(message)s')

# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.DEBUG)
# stream_handler.setFormatter(stream_formatter)

# file_handler = logging.FileHandler(f"{LOG_DIR}/client.log")
# file_handler.setLevel(logging.WARNING)
# file_handler.setFormatter(log_formatter)

# client_logger.addHandler(file_handler)
# client_logger.addHandler(stream_handler)
