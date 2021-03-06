import sys
import traceback
from logging.config import dictConfig
from logging import *

syslog_cfg = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': 'python %(name)s %(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'syslog': {
            'level':'INFO',
            'class':'logging.handlers.SysLogHandler',
            'formatter':'simple',
            'address':'/dev/log',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        '':{
            'handlers': ['syslog','console'],
            'level': 'INFO',
        },
    }
}

dictConfig(syslog_cfg)

exception_logger = getLogger('exception')

def log_exception(cls, val, tb, logger=exception_logger):
    logger.error('Exception:')
    exc = ''.join(traceback.format_exception(cls, val, tb))
    for line in exc.rstrip().split('\n'):
        logger.error(line)
    sys.__excepthook__(cls, val, tb)

sys.excepthook = log_exception
