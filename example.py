#!/usr/bin/env python3

from constant.message_type import ORDER_ACK
from base.connection import start_connection
from base.thread_handler import socket_thread
from oauth.base import get_api_keys
from example_message import (
    create_client_logon,
    create_client_logout,
    create_new_limit_order,
)

message_type = ""

print("This is the example program showing how to use Python binary socket library.\n")
print("1. Specify the IPv4 address and the port number of the server\n")

host = input("Enter a valid IPv4 address: ")
port = input("Enter a valid port number: ")
port = int(port)
# host = "127.0.0.1"
# port = 4444

process_state = "send_logon"


def onMessage(ret, reason, msg, msg_len):
    global process_state
    print("Received message: len=", msg_len)
    if ret is False:
        print("Failed Reason:", reason)
        return

    if msg.Data1 == "H":  # logon message
        if msg.LoginStatus == 1:  # success
            print("Logon success")
            process_state = "send_order"
        elif msg.LoginStatus == 2:  # failure
            print("Logon fail")
            msg.print_reject_reason()
            process_state = "exit"
    elif msg.Data1 == "T":  # order message
        if msg.MessageType == ORDER_ACK:
            print("Order replied")
            process_state = "send_logout"
    else:
        print("Unexpected message:", msg.Data1)


def send_example_messages(socket_controller, api_key):
    global process_state
    if process_state == "send_logon":
        print("\n2. Send the Logon message\n")
        socket_controller.msgObj = create_client_logon(api_key)
        socket_controller.is_send = True
        process_state = "recv_logon"
    elif process_state == "send_order":
        print("\n3. Send the Order message\n")
        socket_controller.msgObj = create_new_limit_order()
        socket_controller.is_send = True
        process_state = "recv_order_reply"
    elif process_state == "send_logout":
        print("\n4. Send the Logout message\n")
        socket_controller.msgObj = create_client_logout()
        socket_controller.is_send = True
        process_state = "exit"
    else:
        socket_controller.is_send = False


sel = start_connection(host, port, onMessage)
api_key = get_api_keys()
socket_thread(sel, process_state, api_key, send_example_messages)

while True:
    pass
