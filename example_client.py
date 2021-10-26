# This is the example client program showing how to use Python binary socket library.

import time
from base.logger import log
from constant.message_type import (
    CANCEL_REPLACE,
    CANCELLED,
    ORDER_ACK,
    ORDER_CANCEL,
    ORDER_NEW,
    QUOTE_FILL,
    REPLACED,
)
from constant.order_type import LMT, OCO_ICE, TPSL_LIMIT
from example_message import (
    create_example_transaction,
)
from base.library_manager import (
    LIB_STATE_SEND_AES_LOGON,
    LibraryManager,
)

message_type = ""

log("This is the example program showing how to use Python binary socket library.")
log("Specify the IPv4 address and the port number of the AES server.")

host = input("Enter a valid IPv4 address: ")
port = input("Enter a valid port number: ")
port = int(port)
# host = "127.0.0.1"
# port = 4444

api_key = input("Enter API Trading Key: ")
user_name = input("Enter User Name: ")
account = int(input("Enter Account: "))


process_state = LIB_STATE_SEND_AES_LOGON


def oes_recv_callback(ret, reason, msg, msg_len):
    """
    It is the receiving callback function for the client socket with OES server.
    """
    global process_state

    if msg.Data1 == "H":  # logon message
        if msg.LoginStatus == 1:  # success
            process_state = "send_transaction"
        elif msg.LoginStatus == 2:  # failure
            process_state = "exit"
    elif msg.Data1 == "T":  # order message
        if msg.MessageType == ORDER_ACK:
            pass
        elif msg.MessageType == CANCELLED:
            pass
        elif msg.MessageType == REPLACED:
            pass
        elif msg.MessageType == QUOTE_FILL:
            pass

    return process_state


transaction_type = ORDER_NEW
order_type = LMT


def oes_send_callback(socket_controller, oes_key, api_key):
    """
    It is the sending callback function for the client socket with OES server.
    """
    global process_state
    global transaction_type
    global order_type

    if process_state != "exit":
        log(
            "Sending the Order message, msg_type=",
            transaction_type,
            "order_type=",
            order_type,
        )
        socket_controller.msgObj = create_example_transaction(
            oes_key, transaction_type, order_type
        )
        socket_controller.is_send = True

        if transaction_type == ORDER_NEW:
            transaction_type = CANCEL_REPLACE
        elif transaction_type == CANCEL_REPLACE:
            transaction_type = ORDER_CANCEL
        elif transaction_type == ORDER_CANCEL:
            transaction_type = ORDER_NEW
            order_type = order_type + 1
            if order_type == OCO_ICE:
                order_type = order_type + 1

            if order_type > TPSL_LIMIT:
                process_state = "exit"

    else:
        socket_controller.is_send = False

    time.sleep(1)


manager = LibraryManager(
    aes_host=host,
    aes_port=port,
    api_key=api_key,
    user_name=user_name,
    account=account,
    oes_recv_callback=oes_recv_callback,
    oes_send_callback=oes_send_callback,
)
manager.start()

while True:
    # log("totp=", totp.now())
    time.sleep(1)
    pass
