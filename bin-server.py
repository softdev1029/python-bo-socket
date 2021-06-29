#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libserverbin
import collateral
import logon
import collateralreq
from auth.client_logon import ClientLogon

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read

    print("accepted connection from", addr)
    conn.setblocking(False)
    # message_logon = libserverbin.MessageWrapper(sel, conn, addr, logon.Logon())
    # sel.register(conn, selectors.EVENT_READ, data=message_logon)

    # collateral_req = collateralreq.CollateralReq()
    # collateral_req.set_data("f", "", 34, 0, 0, 100500, 0, 1, 0, 0, 1623152815)
    # message_collateralreq = libserverbin.MessageWrapper(sel, conn, addr, collateral_req)
    # sel.register(conn, selectors.EVENT_READ, data=message_collateralreq)

    message = ClientLogon()
    message.set_data(
        "H",  # data1
        "1",  # data2
        143,  # data3
        1,  # LogonType
        253336,  # Account
        "1F6A",  # 2FA
        "BOU1",  # UserName
        1,  # TradingSessionID
        "1",  # PrimaryOESIP
        "1",  # SecondaryOESIP
        "1",  # PrimaryMDIP
        "1",  # SecondaryIP
        0,  # SendingTime
        1500201,  # MsgSeqNum
        432451,  # Key
        0,  # LoginStatus
        0,  # RejectReason
        "",  # RiskMaster
    )
    message_wrapper = libserverbin.MessageWrapper(sel, conn, addr, message)
    sel.register(conn, selectors.EVENT_READ, data=message_wrapper)

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
