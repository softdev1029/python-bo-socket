#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libserverbin
import collateral
import logon
import collateralreq

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read
    print("accepted connection from", addr)
    conn.setblocking(False)
    # message_logon = libserverbin.MessageWrapper(sel, conn, addr, logon.Logon())
    # sel.register(conn, selectors.EVENT_READ, data=message_logon)
    collateral_req = collateralreq.CollateralReq()
    collateral_req.set_data("f", "", 34, 0, 0, 100500, 0, 1, 0, 0, 1623152815)
    message_collateralreq = libserverbin.MessageWrapper(sel, conn, addr, collateral_req)
    sel.register(conn, selectors.EVENT_READ, data=message_collateralreq)
    # message_collateral = libserverbin.MessageWrapper(sel, conn, addr, collateral.Collateral())
    # sel.register(conn, selectors.EVENT_READ, data=message_collateral)


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Avoid bind() exception: OSError: [Errno 48] Address already in use
lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
lsock.bind((host, port))
lsock.listen()
print("listening on", (host, port))
lsock.setblocking(False)
sel.register(lsock, selectors.EVENT_READ, data=None)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(key.fileobj)
            else:
                message = key.data
                try:
                    message.process_events(mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{message.addr}:\n{traceback.format_exc()}",
                    )
                    message.close()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
