import time
from base.logger import log
from constant.message_type import CANCELLED, ORDER_ACK, QUOTE_FILL, REPLACED, RISK_REJECT
from example_message import (
    create_transaction,
)
from base.library_manager import (
    LIB_STATE_SEND_AES_LOGON,
    LIB_STATE_SEND_OES_LOGOUT,
    LibraryManager,
)

message_type = ""

log("This is the example program showing how to use Python binary socket library.")
log("Specify the IPv4 address and the port number of the AES server.")

# host = input("Enter a valid IPv4 address: ")
# port = input("Enter a valid port number: ")
# port = int(port)
host = "127.0.0.1"
port = 4444

api_key = input("Enter API Trading Key: ")
user_name = input("Enter User Name: ")
account = int(input("Enter Account: "))


process_state = LIB_STATE_SEND_AES_LOGON

def oes_recv_callback(ret, reason, msg, msg_len):
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

transaction_type = 1

def oes_send_callback(socket_controller, oes_key, api_key):
    global process_state
    global transaction_type

    if process_state != "exit":
        log("Sending the Order message ...")
        socket_controller.msgObj = create_transaction(oes_key, transaction_type)
        socket_controller.is_send = True
        transaction_type = transaction_type + 1

        if transaction_type > RISK_REJECT:
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
    # time.sleep(1)
    pass
