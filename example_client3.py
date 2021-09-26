#!/usr/bin/env python3

from constant.message_type import ORDER_ACK
from base.connection import start_connect_to_server
from base.thread_handler import socket_thread
from example_message import (
    create_client_logon,
    create_client_logout,
    create_new_limit_order,
)
from base.library_manager import (
    LIB_STATE_SEND_AES_LOGON,
    LIB_STATE_SEND_OES_LOGOUT,
    LIB_STATE_SEND_ORDER,
    LibraryManager,
)

message_type = ""

print("This is the example program showing how to use Python binary socket library.\n")
print("1. Specify the IPv4 address and the port number of the server\n")

host = input("Enter a valid IPv4 address: ")
port = input("Enter a valid port number: ")
port = int(port)
# host = "127.0.0.1"
# port = 4444

api_key = input("Enter API Trading Key: ")


process_state = LIB_STATE_SEND_AES_LOGON


def oes_recv_callback(ret, reason, msg, msg_len):
    global process_state
    print("Received message: len=", msg_len)
    if ret is False:
        print("Failed Reason:", reason)
        return

    if msg.Data1 == "H":  # logon message
        if msg.LoginStatus == 1:  # success
            print("OES Logon success")
            process_state = LIB_STATE_SEND_ORDER
        elif msg.LoginStatus == 2:  # failure
            print("OES Logon fail")
            msg.print_reject_reason()
            process_state = "exit"
    elif msg.Data1 == "T":  # order message
        if msg.MessageType == ORDER_ACK:
            print("Order replied")
            process_state = LIB_STATE_SEND_OES_LOGOUT
    else:
        print("Unexpected message:", msg.Data1)

    return process_state


def oes_send_callback(socket_controller, api_key):
    global process_state
    if process_state == LIB_STATE_SEND_ORDER:
        print("\n3. Send the Order message\n")
        socket_controller.msgObj = create_new_limit_order()
        socket_controller.is_send = True
        process_state = "recv_order_reply"
    else:
        socket_controller.is_send = False

    return process_state


manager = LibraryManager(
    aes_host=host,
    aes_port=port,
    api_key=api_key,
    oes_recv_callback=oes_recv_callback,
    oes_send_callback=oes_send_callback,
)
manager.start()

while True:
    # print("totp=", totp.now())
    # time.sleep(1)
    pass
