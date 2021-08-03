from base.message import Message
from auth.client_logon import ClientLogon, create_client_logon
from auth.client_logout import ClientLogout, create_client_logout
from instrument.instrument_request import InstrumentRequest, create_instrument_request
# from auth.risk_update_request import RiskUpdateRequest, create_risk_update_request
from risk.risk_user_symbol import RiskUserSymbol, create_risk_user_symbol
from transaction.open_order_request import OpenOrderRequest, create_open_order_request
from risk.collateral_update import CollateralUpdate, create_collateral_update
# from trade.collateral import Collateral
from transaction.order import Order, create_new_order
from constant import message_type


MESSAGE_TYPES_KEYS = {mt['header']: mt['desc'] for k, mt in message_type.DICT.items()}


def create_message(message_type_desc):
	if message_type_desc == message_type.MSG_CLIENT_LOGON['desc']:
		message = create_client_logon()
	elif message_type_desc == message_type.MSG_CLIENT_LOGOUT['desc']:
		message = create_client_logout()
	elif message_type_desc == message_type.MSG_INSTRUMENT_REQUEST['desc']:
		message = create_instrument_request()
	elif message_type_desc == message_type.MSG_INSTRUMENT_RESPONSE['desc']:
		message = create_instrument_request()
	elif message_type_desc == message_type.MSG_RISK_UPDATE_REQUEST['desc']:
		message = create_risk_user_symbol()
	elif message_type_desc == message_type.MSG_COLLATERAL_RESPONSE['desc']:
		message = create_collateral_update()
	elif message_type_desc == message_type.MSG_RISK_USER_SYMBOL['desc']:
		message = create_risk_user_symbol()
	elif message_type_desc == message_type.MSG_OPEN_ORDER_REQUEST['desc']:
		message = create_open_order_request()
	elif message_type_desc == message_type.MSG_COLLATERAL_REQUEST['desc']:
		message = create_collateral_update()
	elif message_type_desc == message_type.MSG_NEW_ORDER['desc']:
		message = create_new_order()
	else:
		message = Message()
	return message


def is_valid_message_type(message_type_key):
	if message_type_key in MESSAGE_TYPES_KEYS.keys():
		return True

	if message_type_key == "0":
		return True

	return False


def get_all_request_message_types_string():
	res = ""
	res += "0\tGo To Receive Mode\n"
	for k, mt in message_type.DICT.items():
		if mt['request'] is True:
			res += k + "\t" + mt['header'] + "\n"
	return res


def get_message_type_from_header(key):
	if key in MESSAGE_TYPES_KEYS.keys():
		return MESSAGE_TYPES_KEYS[key]
	return ""
