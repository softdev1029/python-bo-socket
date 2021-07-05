from base.message import create_base_message
from auth.client_logon import ClientLogon, create_client_logon
from auth.instrument_request import InstrumentRequest, create_instrument_request
from auth.instrument_response import InstrumentResponse, create_instrument_response
from auth.risk_update_request import RiskUpdateRequest, create_risk_update_request
from auth.risk_user_symbol import RiskUserSymbol, create_risk_user_symbol
from auth.open_order_request import OpenOrderRequest, create_open_order_request
from trade.collateral_request import CollateralRequest, create_collateral_request
from trade.collateral import Collateral
from transaction.new_limit_order import NewLimitOrder, create_new_limit_order

MESSAGE_TYPES = {
    "H": "client_logon",
    "Y": "instrument_request",
    "w": "risk_update_request",
    "N": "risk_user_symbol",
    "E": "open_order_request",
    "f": "collateral_request",
    "T": "new_limit_order",
}


def create_message(message_type):
    if message_type == "client_logon":
        message = create_client_logon()
    elif message_type == "instrument_request":
        message = create_instrument_request()
    elif message_type == "instrument_response":
        message = create_instrument_response()
    elif message_type == "risk_update_request":
        message = create_risk_update_request()
    elif message_type == "risk_user_symbol":
        message = create_risk_user_symbol()
    elif message_type == "open_order_request":
        message = create_open_order_request()
    elif message_type == "collateral_request":
        message = create_collateral_request()
    elif message_type == "new_limit_order":
        message = create_new_limit_order()
    else:
        message = create_base_message()
    return message


def is_valid_message_type(message_type_key):
    if message_type_key in MESSAGE_TYPES.keys():
        return True
    return False


def get_all_message_types_string():
    res = ""
    for i in MESSAGE_TYPES:
        res += i + "\t" + MESSAGE_TYPES[i] + "\n"
    return res


def get_message_type_from_header(key):
    return MESSAGE_TYPES[key]
