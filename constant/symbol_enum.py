BTCUSD = 1
USDUSDT = 2
FLYUSDT = 3
BTCUSDT = 4

from constant import symbol_enum as module_self

DICT = {k: mt for k, mt in module_self.__dict__.items() if not k.startswith('_') and not k.startswith('module_self')}
INVDICT = {mt: k for k, mt in module_self.__dict__.items() if not k.startswith('_') and not k.startswith('module_self') and k != 'DICT'}
