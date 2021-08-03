BUY = 1
SELL = 2
SELLSHORT = 3

from constant import side_type as module_self

DICT = {k: mt for k, mt in module_self.__dict__.items() if not k.startswith('_') and not k.startswith('module_self')}
INVDICT = {mt: k for k, mt in module_self.__dict__.items() if not k.startswith('_') and not k.startswith('module_self') and k != 'DICT'}