#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import initiator_socket_controller

from base.create_message import (
    create_message,
    get_all_request_message_types_string,
    is_valid_message_type,
    REQUEST_MESSAGE_TYPES,
)

sel = selectors.DefaultSelector()

message_type = ""


def start_connection(host, port):
    addr = (host, port)
    print("\nstarting connection to", addr, " ...\n")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)

    msgObj = create_message(message_type)

    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    socket_controller = initiator_socket_controller.InitiatorSocketController(
        sel, sock, addr, msgObj
    )
    sel.register(sock, events, data=socket_controller)


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])

start_connection(host, port)

try:
    while True:
        message_type = ""
        message_type_key = ""
        while is_valid_message_type(message_type_key) is False:

            try:
                message_type_key = input(
                    get_all_request_message_types_string()
                    + "\nEnter a valid message type: "
                )
            except Exception:
                pass

        events = sel.select(timeout=1)
        for key, mask in events:
            socket_controller = key.data
            if message_type_key == "0":
                pass
            else:
                message_type = REQUEST_MESSAGE_TYPES[message_type_key]

                socket_controller.msgObj = create_message(message_type)
                socket_controller.is_send = True
                print("\n")

            try:
                socket_controller.process_events(mask)
            except Exception:
                print(
                    "main: error: exception for",
                    f"{socket_controller.addr}:\n{traceback.format_exc()}",
                )
                socket_controller.close()
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
