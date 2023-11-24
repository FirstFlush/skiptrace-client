import logging
import os
from termcolor import colored
import logging.config
import json

with open('webweaver_cli/config.json', 'r') as f:
    json_settings = json.load(f)



# ENDPOINTS
# ============================================
DOMAIN = json_settings['SERVER']['domain']
LAUNCH_CAMPAIGN_ROUTE = json_settings['SERVER']['endpoints']['launch_campaign']
LAUNCH_SPIDER_ROUTE = json_settings['SERVER']['endpoints']['launch_spider']
LIST_PARAMS_ROUTE = json_settings['SERVER']['endpoints']['list_params']
LIST_SPIDERS_ROUTE = json_settings['SERVER']['endpoints']['list_spiders']
LIST_CAMPAIGNS_ROUTE = json_settings['SERVER']['endpoints']['list_campaigns']
LIST_JOBS_ROUTE = json_settings['SERVER']['endpoints']['list_jobs']
SAVE_JOB_TO_FILE_ROUTE = json_settings['SERVER']['endpoints']['save_job']
CREATE_SPIDER_ROUTE = json_settings['SERVER']['endpoints']['create_spider']
CREATE_PARAMS_ROUTE = json_settings['SERVER']['endpoints']['create_params']

# Debug Status
# ============================================
DEBUG = True


# Constants
# ============================================
LOG_DIR = os.path.join(os.path.dirname(__file__), 'log')
SCRAPING_MODULES_DIR = json_settings['SERVER']['directories']['scraping_modules']

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

if DEBUG is True:
    LOG_LEVEL = "DEBUG"
else:
    LOG_LEVEL = "INFO"

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

