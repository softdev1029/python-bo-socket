import logging
import time

IS_LOGGING=True
IS_FILE=False

if IS_FILE:
    LOG_FILENAME = 'logging_example.out' + str(time.time())
    logging.basicConfig(
        filename=LOG_FILENAME,
        level=logging.DEBUG,
    )

def convertTuple(tup):
    st = ' '.join(map(str, tup))
    return st

def log(*args):
    if IS_LOGGING:
        if IS_FILE:
            logging.debug("[lib] " + convertTuple(args))
        else:
            print("[lib] ", *args)