import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class NewLimitOrder(Message):
    def __init__(self):
        super(NewLimitOrder, self).__init__()
        self.MessageName = "New Limit Order"
        self._names = (
            "Data1",
            "Data2",
            "Data3",
            "MessageType",
            "Padding",
            "Account",
            "OrderID",
            "SymbolEnum",
            "OrderType",
            "SymbolType",
            "BOPrice",
            "BOSide",
            "BOOrderQty",
            "TIF",
            "StopLimitPrice",
            "BOSymbol",
            "OrigOrderID",
            "BOCancelShares",
            "ExecID",
            "ExecShares",
            "RemainingQuantity",
            "ExecFee",
            "ExpirationDate",
            "TraderID",
            "RejectReason",
            "SendingTime",
            "TradingSessionID",
            "Key",
            "DisplaySize",
            "RefreshSize",
            "Layers",
            "SizeIncrement",
            "PriceIncrement",
            "PriceOffset",
            "BOOrigPrice",
            "ExecPrice",
            "MsgSeqNum",
            "TakeProfitPrice",
            "TriggerType",
            "Attributes",
        )

    def make_pack_struct(self):
        return struct.Struct(
            "= 1s 1s H H H I Q H H H d H d H d 12s Q d Q d d d 12s 6s H Q i i d d h d d d d d q d H 12s"
        )


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
    return message
