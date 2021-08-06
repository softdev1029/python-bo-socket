IS_LOGGING=True
def log(*args):
    if IS_LOGGING:
        print("[lib] ", *args)