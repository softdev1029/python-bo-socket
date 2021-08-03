ORDER_NEW = 1
CANCEL_REPLACE = 2
MARGIN_CANCEL_REPLACE = 3
MARGIN_EXECUTE = 4
ORDER_STATUS = 5
ORDER_CANCEL = 6
MARGIN_CANCEL = 7
EXECUTION = 8
EXECUTION_PARTIAL = 9
MARGIN_EXECUTION = 10
MARGIN_PARTIAL_EXECUTION = 11
REJECT = 12
ORDER_REJECT = 13
ORDER_ACK = 14
CANCELLED = 15
REPLACED = 16
QUOTE_FILL = 17
QUOTE_FILL_PARTIAL = 18
MARGIN_REPLACED = 19
CANCEL_REPLACE_REJECT = 20
INSTRUMENT_DATA = 21
INSTRUMENT_RESPONSE = 22
RISK_REJECT = 23

from constant import order_message_type as module_self

DICT = {k: mt for k, mt in module_self.__dict__.items() if not k.startswith('_') and not k.startswith('module_self')}
INVDICT = {mt: k for k, mt in module_self.__dict__.items() if not k.startswith('_') and not k.startswith('module_self') and k != 'DICT'}
