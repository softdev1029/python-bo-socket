#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import client_message_wrapper

from base.create_message import (
    create_message,
    get_all_message_types_string,
    is_valid_message_type,
    MESSAGE_TYPES,
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
    message_wrapper = client_message_wrapper.ClientMessageWrapper(
        sel, sock, addr, msgObj
    )
    sel.register(sock, events, data=message_wrapper)


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])

start_connection(host, port)

try:
    while True:
        message_type = ""
        while is_valid_message_type(message_type) is False:

            try:
                message_type_num = int(
                    input(
                        get_all_message_types_string()
                        + "\nEnter a valid message type: "
                    )
                )

                if message_type_num > 0 and message_type_num <= len(MESSAGE_TYPES):
                    message_type = MESSAGE_TYPES[message_type_num - 1]
            except Exception:
                pass

        print("message type", message_type)
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
            message.msgObj = create_message(message_type)
            print(message.msgObj)
            try:
                message.process_events(mask)
            except Exception:
                print(
                    "main: error: exception for",
                    f"{message.addr}:\n{traceback.format_exc()}",
                )
                message.close()
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
