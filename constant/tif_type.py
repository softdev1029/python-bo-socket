FOK = 1
GTC = 2
IOC = 3
POO = 4
RED = 4
DAY = 5

from constant import tif_type as module_self

DICT = {k: mt for k, mt in module_self.__dict__.items() if not k.startswith('_') and not k.startswith('module_self')}
INVDICT = {mt: k for k, mt in module_self.__dict__.items() if not k.startswith('_') and not k.startswith('module_self') and k != 'DICT'}
