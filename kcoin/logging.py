import os

LOGGING_CONFIG_DICT = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "\n[%(asctime)s] %(levelname)s [%(name)s - Line %(lineno)s]: %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        "simple": {
            'format': "%(levelname)s %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "formatter": "verbose",
            "filename": os.getenv("LOGGING_PATH", "DEBUG.log"),
            "when": "midnight",
            "interval": 1,
            "backupCount": 7
        }
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            'handlers': ["file", "console"],
        },
        'django': {
            'handlers': ["file", "console"],
            'level': 'ERROR',
            'propagate': True
        },
    }
}
