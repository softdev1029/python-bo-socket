"""
This file is for Transaction message
"""

import struct
from base.message import Message
from constant import attribute_type
from constant.types_management import attribute, get_attributes_desc, set_attributes


class Order(Message):
    """
    This class is for Transaction message
    """

    def __init__(self):
        super(Order, self).__init__()
        self.MessageName = "Order"
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
        self.Attributes = ''.join(['N'] * len(attribute))

    def set_attributes(self, *attributes):
        """
        set the attributes as string
        :param attributes: list of enums
        :return:
        """
        try:
            self.Attributes = set_attributes(*attributes)
        except Exception as ex:
            print(ex)

    def get_attributes(self, attribute_data: str) -> list:
        """
        get attribute's description
        :param attribute_data: string
        :return: list of enums
        """
        return get_attributes_desc(attribute_data)

    def make_pack_struct(self):
        """
        build the binary struct for message
        """
        return struct.Struct(
            "= 1s 1s H H H I Q H H H d H d H d 12s Q d Q d d d 12s 6s H Q i i d d h d d d d d q d H d H H 12s"
        )
