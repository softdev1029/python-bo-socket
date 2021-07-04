#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import client_message_wrapper

from base.create_message import create_message

sel = selectors.DefaultSelector()


def start_connection(host, port, message_type):
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


if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <message_type>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
message_type = sys.argv[3]

start_connection(host, port, message_type)

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            message = key.data
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
