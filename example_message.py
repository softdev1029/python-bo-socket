# These example functions tell the library user how to make messages

from auth.client_logon import ClientLogon
from constant.logon_type import (
    LOGIN,
    LOGOUT,
)
from transaction.transaction import Order
from constant import attribute_type
import base64



def create_example_client_logon(aes_or_oes_key, api_key="", user_name="", accont=0):
    """
    This example function tells the library user how to make Client Logon message
    """
    # totp = pyotp.TOTP(base64.b32encode(bytearray(api_key, "ascii")).decode("utf-8"))
    # hotp = pyotp.HOTP(base64.b32encode(bytearray(api_key, "ascii")).decode("utf-8"))

    message = ClientLogon()
    message.login(account=accont, username=user_name, key=aes_or_oes_key, api_key=api_key)
    # message.LogonType = LOGIN
    # message.Account = accont
    # message.TwoFA = hotp.at(0)
    # message.UserName = user_name
    # message.Key = aes_or_oes_key
    # message.set_data(
    #     "H",  # data1
    #     "",  # data2
    #     143,  # data3
    #     1,  # LogonType
    #     accont,  # Account
    #     # totp.now(),  # 2FA
    #     hotp.at(0),
    #     user_name,  # UserName
    #     506,  # TradingSessionID
    #     "1",  # PrimaryOESIP
    #     "1",  # SecondaryOESIP
    #     "1",  # PrimaryMDIP
    #     "1",  # SecondaryIP
    #     0,  # SendingTime
    #     1500201,  # MsgSeqNum
    #     aes_or_oes_key,  # Key
    #     0,  # LoginStatus
    #     0,  # RejectReason
    #     "",  # RiskMaster
    # )

    return message


def create_example_client_logout(aes_or_oes_key):
    """
    This example function tells the library user how to make Client Logout message
    """
    message = ClientLogon()
    message.LogonType = LOGOUT
    message.Key = aes_or_oes_key
    # message.set_data(
    #     "H",  # data1
    #     "",  # data2
    #     143,  # data3
    #     2,  # LogonType
    #     100700,  # Account
    #     "1F6A",  # 2FA
    #     "BOU7",  # UserName
    #     506,  # TradingSessionID
    #     "1",  # PrimaryOESIP
    #     "1",  # SecondaryOESIP
    #     "1",  # PrimaryMDIP
    #     "1",  # SecondaryIP
    #     0,  # SendingTime
    #     1500201,  # MsgSeqNum
    #     aes_or_oes_key,  # Key
    #     0,  # LoginStatus
    #     0,  # RejectReason
    #     "",  # RiskMaster
    # )
    return message


def create_example_transaction(aes_or_oes_key, type, orderType):
    """
    This example function tells the library user how to make Transaction message
    """
    message = Order()
    message.OrderType = orderType
    message.BOSymbol = "BTCUSD"
    message.Key = aes_or_oes_key
    message.set_attributes(attribute_type.HIDDEN_TYPE)

    # message.set_data(
    #     "T",  # data1,
    #     "",  # data2,
    #     250,  # data3,
    #     type,  # messageType
    #     0,  # padding,
    #     100700,  # account,
    #     46832151,  # orderID,
    #     1,  # symbolEnum,
    #     orderType,  # OrderType LMT
    #     1,  # SymbolType SPOT
    #     50100.5,  # BOPrice,
    #     3,  # BOSide BUY
    #     2.0,  # BOOrderQty,
    #     2,  # TIF -> GTC
    #     0,  # StopLimitPrice,
    #     "BTCUSD",  # BOSymbol,
    #     0,  # OrigOrderID,
    #     0,  # BOCancelShares,
    #     0,  # ExecID,
    #     0,  # ExecShares,
    #     0,  # RemainingQuantity,
    #     0,  # ExecFee,
    #     "",  # ExpirationDate,
    #     "",  # TraderID,
    #     0,  # RejectReason,
    #     1000,  # SendingTime,
    #     506,  # TradingSessionID,
    #     aes_or_oes_key,  # Key,
    #     0,  # DisplaySize,
    #     0,  # RefreshSize,
    #     0,  # Layers,
    #     0,  # SizeIncrement,
    #     0,  # PriceIncrement,
    #     0,  # PriceOffset,
    #     0,  # BOOrigPrice,
    #     0,  # ExecPrice,
    #     79488880,  # MsgSeqNum,
    #     0,  # TakeProfitPrice,
    #     0,  # TriggerType,
    #     1111,  # SecondLegPrice,
    #     1,  # RouteEnum,
    #     1,  # ModifyType,
    #     "",  # Attributes,
    # )
    return message
