#!/usr/bin/env python3

from constant.message_type import ORDER_ACK
from base.connection import start_connect_to_server
from base.thread_handler import socket_thread
from oauth.base import get_api_keys
from example_message import (
    create_client_logon,
    create_client_logout,
    create_new_limit_order,
)
import pyotp
import time
import base64

message_type = ""

print("This is the example program showing how to use Python binary socket library.\n")
print("1. Specify the IPv4 address and the port number of the server\n")

host = input("Enter a valid IPv4 address: ")
port = input("Enter a valid port number: ")
port = int(port)
# host = "127.0.0.1"
# port = 4444

process_state = "send_aes_logon"
api_key = ""


def aes_recv_callback(ret, reason, msg, msg_len):
    global process_state
    global api_key
    print("Received message: len=", msg_len)
    if ret is False:
        print("Failed Reason:", reason)
        return

    if msg.Data1 == "H":  # logon message
        if msg.LoginStatus == 1:  # success
            print("AES Logon success")

            oes_ip = msg.PrimaryOrderEntryIP.split(":")
            if len(oes_ip) == 2:
                host = oes_ip[0]
                port = int(oes_ip[1].rstrip("\x00"))
                sel = start_connect_to_server(host, port, oes_recv_callback)
                socket_thread(sel, process_state, api_key, oes_send_callback)

                process_state = "send_order"
            else:
                print("AES Logon fail, invalid OES IP")
                process_state = "exit"
        elif msg.LoginStatus == 2:  # failure
            print("AES Logon fail")
            msg.print_reject_reason()
            process_state = "exit"
    else:
        print("Unexpected message:", msg.Data1)


def aes_send_callback(socket_controller, api_key):
    global process_state
    if process_state == "send_aes_logon":
        print("\n2. Send the AES Logon message\n")
        socket_controller.msgObj = create_client_logon(api_key)
        socket_controller.is_send = True
        process_state = "recv_logon"
    elif process_state == "send_aes_logout":
        print("\n4. Send the AES Logout message\n")
        socket_controller.msgObj = create_client_logout()
        socket_controller.is_send = True
        process_state = "exit"
    else:
        socket_controller.is_send = False


def oes_recv_callback(ret, reason, msg, msg_len):
    global process_state
    print("Received message: len=", msg_len)
    if ret is False:
        print("Failed Reason:", reason)
        return

    if msg.Data1 == "H":  # logon message
        if msg.LoginStatus == 1:  # success
            print("OES Logon success")
            process_state = "send_order"
        elif msg.LoginStatus == 2:  # failure
            print("OES Logon fail")
            msg.print_reject_reason()
            process_state = "exit"
    elif msg.Data1 == "T":  # order message
        if msg.MessageType == ORDER_ACK:
            print("Order replied")
            process_state = "send_logout"
    else:
        print("Unexpected message:", msg.Data1)


def oes_send_callback(socket_controller, api_key):
    global process_state
    if process_state == "send_oes_logon":
        print("\n2. Send the OES Logon message\n")
        socket_controller.msgObj = create_client_logon(api_key)
        socket_controller.is_send = True
        process_state = "recv_logon"
    elif process_state == "send_order":
        print("\n3. Send the Order message\n")
        socket_controller.msgObj = create_new_limit_order()
        socket_controller.is_send = True
        process_state = "recv_order_reply"
    elif process_state == "send_oes_logout":
        print("\n4. Send the OES Logout message\n")
        socket_controller.msgObj = create_client_logout()
        socket_controller.is_send = True
        process_state = "exit"
    else:
        socket_controller.is_send = False


sel = start_connect_to_server(host, port, aes_recv_callback)

# api_key = get_api_keys()
api_key = input("Enter API Trading Key: ")

socket_thread(sel, process_state, api_key, aes_send_callback)

totp = pyotp.TOTP(base64.b32encode(bytearray(api_key, "ascii")).decode("utf-8"))
hotp = pyotp.HOTP(base64.b32encode(bytearray(api_key, "ascii")).decode("utf-8"))
# print("hotp=", hotp.at(0))


while True:
    # print("totp=", totp.now())
    # time.sleep(1)
    pass
