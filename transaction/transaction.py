# This file is for Transaction message

import struct
from base.message import Message
from constant.constant import (
    TRANSACTION_ATTRIBUTE_LEN,
    TRANSACTION_ATTRIBUTE_N,
    TRANSACTION_ATTRIBUTE_Y,
)


class Transaction(Message):
    """
    This class is for Transaction message
    """

    def __init__(self):
        super(Transaction, self).__init__()
        self.MessageName = "Transaction"
        self._names = (
            "Data1",
            "Data2",
            "MessageLen",
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

        self.Data1 = "T"
        self.MessageLen = 250
        self.Attributes = [
            TRANSACTION_ATTRIBUTE_N for i in range(TRANSACTION_ATTRIBUTE_LEN)
        ]

    def setAttributes(self, position, value):
        if position < 0 or position >= TRANSACTION_ATTRIBUTE_LEN:
            return

        if value != TRANSACTION_ATTRIBUTE_Y and value != TRANSACTION_ATTRIBUTE_N:
            return

        self.Attributes[position] = value

    def make_pack_struct(self):
        """
        build the binary struct for message
        """
        return struct.Struct(
            "= 1s 1s H H H I Q H H H d H d H d 12s Q d Q d d d 12s 6s H Q i i d d h d d d d d q d H d H H 12s"
        )
