#!/usr/bin/env python3

import sys
import socket
import selectors
import traceback

import libserverbin
from auth.client_logon import ClientLogon
from auth.instrument_request import InstrumentRequest
from auth.instrument_response import InstrumentResponse
from auth.risk_update_request import RiskUpdateRequest
from auth.risk_user_symbol import RiskUserSymbol
from trade.collateral_request import CollateralRequest
from trade.collateral import Collateral
from transaction.new_limit_order import NewLimitOrder

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
    #     "",  # data2
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

    # message = InstrumentRequest()
    # message.set_data(
    #     "Y",  # data1
    #     "",  # data2
    #     62,  # data3
    #     0,  # MessageType
    #     0,  # RejectReason
    #     100700,  # Account
    #     2,  # RequestType
    #     0,  # Key
    #     "",  # SymbolName
    #     0,  # SymbolType
    #     0,  # SymbolEnum
    #     506,  # TradingSessionID
    #     0,  # SendingTime
    #     1500201,  # MsgSeqNum
    # )

    # message = InstrumentResponse()
    # message.set_data(
    #     "Y",  # data1
    #     "",  # data2
    #     62,  # data3
    #     59,  # MessageType, not really required since a message of this type is defined in the first byte of the header
    #     0,  # Padding
    #     2,  # ResponseType
    #     1,  # SymbolEnum
    #     "BTCUSD",  # SymbolName
    #     1,  # SymbolType
    #     0.5,  # PriceIncrement
    #     0.00001,  # MinSize
    #     1000,  # MaxSize
    #     0,  # SendingTime
    #     1500201,  # MsgSeqNum
    # )

    # message = RiskUpdateRequest()
    # message.set_data(
    #     "w",  # data1
    #     "",  # data2
    #     34,  # data3
    #     0,  # MessageType
    #     2,  # ResponseType
    #     10070,  # account
    #     506,  # tradingSessionID
    #     1,  # SymbolEnum
    #     0,  # Key
    #     1005231,  # MsgSeqNum
    #     0,  # SendingTime
    # )

    # message = RiskUserSymbol()
    # message.set_data(
    #     "N",  # data1
    #     "",  # data2
    #     34,  # data3
    #     0,  # MessageType
    #     0,  # Padding
    #     "NAM1",  # UserName
    #     100700,  # Account
    #     1,  # SymbolEnum
    #     0,  # Leverage
    #     3.0,  # LongPosition
    #     5.0,  # ShortPosition
    #     51000,  # LongCash
    #     52000,  # ShortCash
    #     0,  # SymbolDisabled
    #     0,  # AccountEquity
    #     0,  # InstrumentEquity
    #     150000,  # ExecutedLongCash
    #     3,  # ExecutedLongPosition
    #     102000,  # ExecutedShortCash
    #     2,  # ExecutedShortPosition
    #     25,  # BTCEquity
    #     500000,  # USDTEquty
    #     1000,  # ETHEquity
    #     1000000,  # USDEquity
    #     400000,  # FLYEquity
    #     1000,  # OpenOderRequestLimit
    #     506,  # TradingSessionID
    #     42431,  # MsgSeqNum
    # )

    message = NewLimitOrder()
    message.set_data(
        "T",  # data1,
        "",  # data2,
        238,  # data3,
        1,  # messageType ORDER_NEW
        0,  # padding,
        100700,  # account,
        46832151,  # orderID,
        1,  # symbolEnum,
        1,  # OrderType LMT
        1,  # SymbolType SPOT
        50100.5,  # BOPrice,
        1,  # BOSide BUY
        2.0,  # BOOrderQty,
        2,  # TIF -> GTC
        0,  # StopLimitPrice,
        "BTCUSD",  # BOSymbol,
        0,  # OrigOrderID,
        0,  # BOCancelShares,
        0,  # ExecID,
        0,  # ExecShares,
        0,  # RemainingQuantity,
        0,  # ExecFee,
        "",  # ExpirationDate,
        "",  # TraderID,
        0,  # RejectReason,
        1000,  # SendingTime,
        506,  # TradingSessionID,
        42341,  # Key,
        0,  # DisplaySize,
        0,  # RefreshSize,
        0,  # Layers,
        0,  # SizeIncrement,
        0,  # PriceIncrement,
        0,  # PriceOffset,
        0,  # BOOrigPrice,
        0,  # ExecPrice,
        79488880,  # MsgSeqNum,
        0,  # TakeProfitPrice,
        0,  # TriggerType,
        "",  # Attributes,
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
