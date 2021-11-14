"""
This file is related to processing messages such as creating/validation.
"""

from constant.order_message_type import ORDER_NEW
from constant.order_type import LMT
from constant.types_management import message, request_message
from constant.message_type import (
    MSG_CLIENT_LOGON,
    MSG_INSTRUMENT_REQUEST,
    MSG_INSTRUMENT_RESPONSE,
    MSG_RISK_UPDATE_REQUEST,
    MSG_RISK_USER_SYMBOL,
    MSG_OPEN_ORDER_REQUEST,
    MSG_COLLATERAL_REQUEST,
    MSG_TRANSACTION,
    MSG_MD_SUBSCRIBE,
    MSG_MD_EXEC_REPORT,
    MSG_TOB_MSG,
    MSG_THREE_LEVEL_DATA,
    MSG_FIVE_LEVEL_DATA,
    MSG_TEN_LEVEL_DATA,
    MSG_TWENTY_LEVEL_DATA,
    MSG_THIRTY_LEVEL_DATA
    )

from market.five_level_data import create_example_five_level_data
from market.ten_level_data import create_example_ten_level_data
from market.twenty_level_data import create_example_twenty_level_data
from market.thirty_level_data import create_example_thirty_level_data
from market.three_level_data import create_example_three_level_data
from market.tob_msg import create_example_tob_msg
from market.md_exec_report import create_example_md_exec_report
from base.message import Message, create_example_base_message
from example_message import create_example_client_logon
from auth.instrument_request import create_example_instrument_request
from auth.instrument_response import create_example_instrument_response
from auth.risk_update_request import create_example_risk_update_request
from auth.risk_user_symbol import create_example_risk_user_symbol
from auth.open_order_request import create_example_open_order_request
from trade.collateral_request import create_example_collateral_request
from market.md_subscribe import create_example_md_subscribe
from example_message import create_example_transaction


def create_example_message(
    aes_or_oes_key: str, message_type: str, transaction_type=ORDER_NEW, order_type=LMT
) -> Message:
    """
    Create a message according to the type of message.
    All message needs AES/OES key.
    """

    if message_type == MSG_CLIENT_LOGON:
        message = create_example_client_logon(aes_or_oes_key)
    elif message_type == MSG_INSTRUMENT_REQUEST:
        message = create_example_instrument_request(aes_or_oes_key)
    elif message_type == MSG_INSTRUMENT_RESPONSE:
        message = create_example_instrument_response(aes_or_oes_key)
    elif message_type == MSG_RISK_UPDATE_REQUEST:
        message = create_example_risk_update_request(aes_or_oes_key)
    elif message_type == MSG_RISK_USER_SYMBOL:
        message = create_example_risk_user_symbol(aes_or_oes_key)
    elif message_type == MSG_OPEN_ORDER_REQUEST:
        message = create_example_open_order_request(aes_or_oes_key)
    elif message_type == MSG_COLLATERAL_REQUEST:
        message = create_example_collateral_request(aes_or_oes_key)
    elif message_type == MSG_TRANSACTION:
        message = create_example_transaction(
            aes_or_oes_key, transaction_type, order_type
        )
    elif message_type == MSG_MD_SUBSCRIBE:
        message = create_example_md_subscribe(aes_or_oes_key)
    elif message_type == MSG_MD_EXEC_REPORT:
        message = create_example_md_exec_report(aes_or_oes_key)
    elif message_type == MSG_TOB_MSG:
        message = create_example_tob_msg(aes_or_oes_key)
    elif message_type == MSG_THREE_LEVEL_DATA:
        message = create_example_three_level_data(aes_or_oes_key)
    elif message_type == MSG_FIVE_LEVEL_DATA:
        message = create_example_five_level_data(aes_or_oes_key)
    elif message_type == MSG_TEN_LEVEL_DATA:
        message = create_example_ten_level_data(aes_or_oes_key)
    elif message_type == MSG_TWENTY_LEVEL_DATA:
        message = create_example_twenty_level_data(aes_or_oes_key)
    elif message_type == MSG_THIRTY_LEVEL_DATA:
        message = create_example_thirty_level_data(aes_or_oes_key)
    else:
        message = create_example_base_message()
    return message


def is_valid_message_type(message_type_key: str) -> bool:
    """
    Check if the type of message is valid
    """
    if message.is_valid(message_type_key):
        return True

    if message_type_key == "0":
        return True

    return False


def get_all_request_message_types_string() -> str:
    """
    Make the help string for message types
    """
    res = ""
    res += "0\tGo To Receive Mode\n"
    res += str(request_message)
    return res


def get_message_type_from_header(key):
    """
    Get the message type from the value of binary message header
    """

    return key
