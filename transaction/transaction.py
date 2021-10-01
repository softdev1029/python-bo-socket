import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class Transaction(Message):
    def __init__(self):
        super(Transaction, self).__init__()
        self.MessageName = "Transaction"
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
            "SecondLegPrice",
            "RouteEnum",
            "ModifyType",
            "Attributes",
        )

    def make_pack_struct(self):
        return struct.Struct(
            "= 1s 1s H H H I Q H H H d H d H d 12s Q d Q d d d 12s 6s H Q i i d d h d d d d d q d H d H H 12s"
        )
