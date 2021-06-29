#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libclientbin

sel = selectors.DefaultSelector()


def create_request(value):
    print(len(value.encode('utf-8')))
    return dict(
        type="binary/custom-client-binary-type",
        encoding="binary",
        content=value.encode('utf-8'),
    )


def start_connection(host, port, request):
    addr = (host, port)
    print("\nstarting connection to", addr, " ...\n")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    message = libclientbin.MessageWrapper(sel, sock, addr, request)
    sel.register(sock, events, data=message)


if len(sys.argv) != 4:
    print("usage:", sys.argv[0], "<host> <port> <value>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
value = sys.argv[3]
request = create_request(value)
start_connection(host, port, request)

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
