from auth.client_logon import ClientLogon
from transaction.new_limit_order import NewLimitOrder
import pyotp
import base64


def create_client_logon(api_key):
    totp = pyotp.TOTP(base64.b32encode(bytearray(api_key, "ascii")).decode("utf-8"))
    hotp = pyotp.HOTP(base64.b32encode(bytearray(api_key, "ascii")).decode("utf-8"))

    message = ClientLogon()
    message.set_data(
        "H",  # data1
        "",  # data2
        143,  # data3
        1,  # LogonType
        100700,  # Account
        # totp.now(),  # 2FA
        hotp.at(0),
        "BOU7",  # UserName
        506,  # TradingSessionID
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
    message.print_message()

    return message


def create_client_logout():
    message = ClientLogon()
    message.set_data(
        "H",  # data1
        "",  # data2
        143,  # data3
        2,  # LogonType
        100700,  # Account
        "1F6A",  # 2FA
        "BOU7",  # UserName
        506,  # TradingSessionID
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
    return message


def create_new_limit_order():
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
        3,  # BOSide BUY
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
    message.print_message()
    return message
