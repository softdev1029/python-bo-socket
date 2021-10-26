# This file is for defining the library logger

import logging
import time

IS_LOGGING = True
IS_FILE = False

if IS_FILE:
    LOG_FILENAME = "logging_example.out" + str(time.time())
    logging.basicConfig(
        filename=LOG_FILENAME,
        level=logging.DEBUG,
    )


def convertTuple(tup):
    st = " ".join(map(str, tup))
    return st


def logConfig(
    isLogging=True, isFile=False, filename="logging_example.out", level=logging.DEBUG
):
    global IS_LOGGING
    global IS_FILE
    IS_LOGGING = isLogging
    IS_FILE = isFile
    if IS_FILE:
        logging.basicConfig(
            filename=filename,
            level=level,
        )


def log(*args):
    if IS_LOGGING:
        if IS_FILE:
            logging.debug("[lib] " + convertTuple(args))
        else:
            print("[lib] ", *args)
