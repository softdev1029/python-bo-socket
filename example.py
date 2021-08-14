#!/usr/bin/env python3

from constant.message_type import ORDER_ACK
import sys
import traceback

from base.connection import start_connection
from example_message import (
    create_client_logon,
    create_client_logout,
    create_new_limit_order,
)

message_type = ""

print("This is the example program showing how to use Python binary socket library.\n")
print("1. Specify the IPv4 address and the port number of the server\n")

host = input("Enter a valid a IPv4 address: ")
port = input("Enter a valid a port number: ")
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


sel = start_connection(host, port, onMessage)

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            socket_controller = key.data

            if process_state == "send_logon":
                print("\n2. Send the Logon message\n")
                socket_controller.msgObj = create_client_logon()
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

            try:
                socket_controller.process_events(mask)
            except Exception:
                print(
                    "main: error: exception for",
                    f"{socket_controller.addr}:\n{traceback.format_exc()}",
                )
                socket_controller.close()

        if process_state == "exit":
            break

        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
