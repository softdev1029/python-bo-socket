from base.logger import log
from constant.message_type import CANCELLED, ORDER_ACK, QUOTE_FILL, REPLACED
from example_message import (
    create_cancel_replace,
    create_new_limit_order,
)
from base.library_manager import (
    LIB_STATE_SEND_AES_LOGON,
    LIB_STATE_SEND_OES_LOGOUT,
    LIB_STATE_SEND_NEW_ORDER,
    LIB_STATE_SEND_CANCEL_REPLACE,
    LibraryManager,
)

message_type = ""

log("This is the example program showing how to use Python binary socket library.\n")
log("1. Specify the IPv4 address and the port number of the server\n")

# host = input("Enter a valid IPv4 address: ")
# port = input("Enter a valid port number: ")
# port = int(port)
host = "127.0.0.1"
port = 4444

api_key = input("Enter API Trading Key: ")
user_name = input("Enter User Name: ")
account = int(input("Enter Account: "))


process_state = LIB_STATE_SEND_AES_LOGON
counter = 0


def oes_recv_callback(ret, reason, msg, msg_len):
    global process_state
    global counter
    log("Received message: len=", msg_len)
    if ret is False:
        log("Failed Reason:", reason)
        return

    if msg.Data1 == "H":  # logon message
        if msg.LoginStatus == 1:  # success
            log("OES Logon success")
            process_state = LIB_STATE_SEND_NEW_ORDER
        elif msg.LoginStatus == 2:  # failure
            log("OES Logon fail")
            msg.print_reject_reason()
            process_state = "exit"
    elif msg.Data1 == "T":  # order message
        if msg.MessageType == ORDER_ACK:
            log("Order replied")
            process_state = LIB_STATE_SEND_CANCEL_REPLACE
            counter = counter - 1
        elif msg.MessageType == CANCELLED:
            log("Order cancelled")
            process_state = LIB_STATE_SEND_OES_LOGOUT
            counter = counter - 1
        elif msg.MessageType == REPLACED:
            log("Order replaced")
            process_state = LIB_STATE_SEND_OES_LOGOUT
            counter = counter - 1
        elif msg.MessageType == QUOTE_FILL:
            log("Order quote filled")
            process_state = LIB_STATE_SEND_OES_LOGOUT
            counter = counter - 1
    else:
        log("Unexpected message:", msg.Data1)

    return process_state


def oes_send_callback(socket_controller, oes_key, api_key):
    global process_state
    global counter
    if process_state == LIB_STATE_SEND_NEW_ORDER:
        log("Send the New Order message\n")
        socket_controller.msgObj = create_new_limit_order(oes_key)
        socket_controller.is_send = True
        counter = counter + 1
    if process_state == LIB_STATE_SEND_CANCEL_REPLACE:
        log("Send the Cancel Replace message\n")
        socket_controller.msgObj = create_cancel_replace(oes_key)
        socket_controller.is_send = True
        counter = counter + 1
    else:
        socket_controller.is_send = False


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
