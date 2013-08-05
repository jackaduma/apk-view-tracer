#! python2.7
## -*- coding: utf-8 -*-

## kun for Apk View Tracing
## Logger.py

import logging
import logging.handlers

LEVELS={'notset':logging.DEBUG,
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'critical':logging.CRITICAL}

LOG_BACKUPCOUNT = 10
LOG_LEVEL = 'notset'

def InitLog(file_name,logger=None):
    if None == logger:
        logger = logging.getLogger()
    handler = logging.handlers.RotatingFileHandler(file_name,maxBytes=10*1024*1024,backupCount=LOG_BACKUPCOUNT)
    #handler = logging.FileHandler(file_name)
    formatter = logging.Formatter("[ %(asctime)s ][ %(levelname)s ] %(message)s\n")
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(LEVELS.get(LOG_LEVEL.lower()))
    return logger