from market.five_level_data import create_five_level_data
from market.ten_level_data import create_ten_level_data
from market.twenty_level_data import create_twenty_level_data
from market.three_level_data import create_three_level_data
from market.tob_msg import create_tob_msg
from market.md_exec_report import create_md_exec_report
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
from market.md_subscribe import create_md_subscribe

MSG_CLIENT_LOGON = "client_logon"
MSG_INSTRUMENT_REQUEST = "instrument_request"
MSG_INSTRUMENT_RESPONSE = "instrument_response"
MSG_RISK_UPDATE_REQUEST = "risk_update_request"
MSG_RISK_USER_SYMBOL = "risk_user_symbol"
MSG_OPEN_ORDER_REQUEST = "open_order_request"
MSG_COLLATERAL_REQUEST = "collateral_request"
MSG_NEW_LIMIT_ORDER = "new_limit_order"
MSG_MD_SUBSCRIBE = "md_subscribe"
MSG_MD_EXEC_REPORT = "md_exec_report"
MSG_TOB_MSG = "tob_msg"
MSG_THREE_LEVEL_DATA = "three_level_data"
MSG_FIVE_LEVEL_DATA = "five_level_data"
MSG_TEN_LEVEL_DATA = "ten_level_data"
MSG_TWENTY_LEVEL_DATA = "twenty_level_data"

REQUEST_MESSAGE_TYPES = {
    "H": MSG_CLIENT_LOGON,
    "Y": MSG_INSTRUMENT_REQUEST,
    "w": MSG_RISK_UPDATE_REQUEST,
    "E": MSG_OPEN_ORDER_REQUEST,
    "f": MSG_COLLATERAL_REQUEST,
    "T": MSG_NEW_LIMIT_ORDER,
    "s": MSG_MD_SUBSCRIBE,
    "V": MSG_MD_EXEC_REPORT,
    "t": MSG_TOB_MSG,
    "M": MSG_THREE_LEVEL_DATA,
    "m": MSG_FIVE_LEVEL_DATA,
    "O": MSG_TEN_LEVEL_DATA,
    "S": MSG_TWENTY_LEVEL_DATA,
}

MESSAGE_TYPES = {
    "H": MSG_CLIENT_LOGON,
    "Y": MSG_INSTRUMENT_REQUEST,
    "w": MSG_RISK_UPDATE_REQUEST,
    "N": MSG_RISK_USER_SYMBOL,
    "E": MSG_OPEN_ORDER_REQUEST,
    "f": MSG_COLLATERAL_REQUEST,
    "T": MSG_NEW_LIMIT_ORDER,
    "s": MSG_MD_SUBSCRIBE,
    "V": MSG_MD_EXEC_REPORT,
    "t": MSG_TOB_MSG,
    "M": MSG_THREE_LEVEL_DATA,
    "m": MSG_FIVE_LEVEL_DATA,
    "O": MSG_TEN_LEVEL_DATA,
    "S": MSG_TWENTY_LEVEL_DATA,
}


def create_message(message_type):
    if message_type == MSG_CLIENT_LOGON:
        message = create_client_logon()
    elif message_type == MSG_INSTRUMENT_REQUEST:
        message = create_instrument_request()
    elif message_type == MSG_INSTRUMENT_RESPONSE:
        message = create_instrument_response()
    elif message_type == MSG_RISK_UPDATE_REQUEST:
        message = create_risk_update_request()
    elif message_type == MSG_RISK_USER_SYMBOL:
        message = create_risk_user_symbol()
    elif message_type == MSG_OPEN_ORDER_REQUEST:
        message = create_open_order_request()
    elif message_type == MSG_COLLATERAL_REQUEST:
        message = create_collateral_request()
    elif message_type == MSG_NEW_LIMIT_ORDER:
        message = create_new_limit_order()
    elif message_type == MSG_MD_SUBSCRIBE:
        message = create_md_subscribe()
    elif message_type == MSG_MD_EXEC_REPORT:
        message = create_md_exec_report()
    elif message_type == MSG_TOB_MSG:
        message = create_tob_msg()
    elif message_type == MSG_THREE_LEVEL_DATA:
        message = create_three_level_data()
    elif message_type == MSG_FIVE_LEVEL_DATA:
        message = create_five_level_data()
    elif message_type == MSG_TEN_LEVEL_DATA:
        message = create_ten_level_data()
    elif message_type == MSG_TWENTY_LEVEL_DATA:
        message = create_twenty_level_data()
    else:
        message = create_base_message()
    return message


def is_valid_message_type(message_type_key):
    if message_type_key in MESSAGE_TYPES.keys():
        return True

    if message_type_key == "0":
        return True

    return False


def get_all_request_message_types_string():
    res = ""
    res += "0\tGo To Receive Mode\n"
    for i in REQUEST_MESSAGE_TYPES:
        res += i + "\t" + REQUEST_MESSAGE_TYPES[i] + "\n"
    return res


def get_message_type_from_header(key):
    if key in MESSAGE_TYPES.keys():
        return MESSAGE_TYPES[key]
    return ""
