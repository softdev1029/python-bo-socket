#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libserverbin
from auth.client_logon import ClientLogon
from trade.instrument_request import InstrumentRequest
from trade.collateral_request import CollateralRequest
from trade.collateral import Collateral

sel = selectors.DefaultSelector()


def accept_wrapper(sock):
    conn, addr = sock.accept()  # Should be ready to read

    print("accepted connection from", addr)
    conn.setblocking(False)

    # message = CollateralRequest()
    # message.set_data("f", "", 34, 0, 0, 100500, 0, 1, 0, 0, 1623152815)

    # message = ClientLogon()
    # message.set_data(
    #     "H",  # data1
    #     "1",  # data2
    #     143,  # data3
    #     1,  # LogonType
    #     253336,  # Account
    #     "1F6A",  # 2FA
    #     "BOU1",  # UserName
    #     1,  # TradingSessionID
    #     "1",  # PrimaryOESIP
    #     "1",  # SecondaryOESIP
    #     "1",  # PrimaryMDIP
    #     "1",  # SecondaryIP
    #     0,  # SendingTime
    #     1500201,  # MsgSeqNum
    #     432451,  # Key
    #     0,  # LoginStatus
    #     0,  # RejectReason
    #     "",  # RiskMaster
    # )

    message = InstrumentRequest()
    message.set_data(
        "Y",  # data1
        "",  # data2
        62,  # data3
        0,  # MessageType
        0,  # RejectReason
        100700,  # Account
        2,  # RequestType
        0,  # Key
        "",  # SymbolName
        0,  # SymbolType
        0,  # SymbolEnum
        506,  # TradingSessionID
        0,  # SendingTime
        1500201,  # MsgSeqNum
    )

    message_wrapper = libserverbin.MessageWrapper(sel, conn, addr, message)
    sel.register(conn, selectors.EVENT_READ, data=message_wrapper)


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
