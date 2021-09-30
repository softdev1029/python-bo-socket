import logging
import time

LOG_FILENAME = 'logging_example.out' + str(time.time())
logging.basicConfig(
    filename=LOG_FILENAME,
    level=logging.DEBUG,
)

IS_LOGGING=True
IS_FILE=True

def convertTuple(tup):
    st = ' '.join(map(str, tup))
    return st

def log(*args):
    if IS_LOGGING:
        if IS_FILE:
            logging.debug("[lib] " + convertTuple(args))
        else:
            print("[lib] ", *args)