MSG_CLIENT_LOGON = {'header': "H", 'desc': "client_logon", 'request': True, 'response': True}
MSG_CLIENT_LOGOUT = {'header': "H", 'desc': "client_logout", 'request': True, 'response': True}
MSG_INSTRUMENT_REQUEST = {'header': "Y", 'desc': "instrument_request", 'request': True, 'response': False}
MSG_INSTRUMENT_RESPONSE = {'header': 'Q', 'desc': "instrument_response", 'request': False, 'response': True}
MSG_RISK_UPDATE_REQUEST = {'header': "w", 'desc': "risk_update_request", 'request': True, 'response': False}
MSG_RISK_USER_SYMBOL = {'header': "N", 'desc': "risk_user_symbol", 'request': False, 'response': True}
MSG_OPEN_ORDER_REQUEST = {'header': "e", 'desc': "open_order_request", 'request': True, 'response': False}
MSG_COLLATERAL_REQUEST = {'header': "f", 'desc': "collateral_request", 'request': True, 'response': False}
MSG_COLLATERAL_RESPONSE = {'header': "h", 'desc': "collateral_response", 'request': False, 'response': True}
MSG_NEW_ORDER = {'header': "T", 'desc': "new_order", 'request': True, 'response': True}

from constant import message_type as module_self

DICT = {k: mt for k, mt in module_self.__dict__.items() if not k.startswith('_') and not k.startswith('module_self')}

