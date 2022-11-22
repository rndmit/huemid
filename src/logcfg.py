LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
        },
    },

    'loggers': {
        'main': {
            'handlers': ['stream_handler'],
            'level': 'INFO',
            'propagate': True
        }
    }
}
