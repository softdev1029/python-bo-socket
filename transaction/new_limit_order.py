import struct
from utils.helper import print_bytes_hex
from base.message import Message


class NewLimitOrder(Message):
    def __init__(self):
        self.data = ()
        self.binary_data = None

    def set_data(
        self,
        data1,
        data2,
        data3,
        messageType,
        padding,
        account,
        orderID,
        symbolEnum,
        OrderType,
        SymbolType,
        BOPrice,
        BOSide,
        BOOrderQty,
        TIF,
        StopLimitPrice,
        BOSymbol,
        OrigOrderID,
        BOCancelShares,
        ExecID,
        ExecShares,
        RemainingQuantity,
        ExecFee,
        ExpirationDate,
        TraderID,
        RejectReason,
        SendingTime,
        TradingSessionID,
        Key,
        DisplaySize,
        RefreshSize,
        Layers,
        SizeIncrement,
        PriceIncrement,
        PriceOffset,
        BOOrigPrice,
        ExecPrice,
        MsgSeqNum,
        TakeProfitPrice,
        TriggerType,
        Attributes,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            messageType,
            padding,
            account,
            orderID,
            symbolEnum,
            OrderType,
            SymbolType,
            BOPrice,
            BOSide,
            BOOrderQty,
            TIF,
            StopLimitPrice,
            BOSymbol.encode("utf-8"),
            OrigOrderID,
            BOCancelShares,
            ExecID,
            ExecShares,
            RemainingQuantity,
            ExecFee,
            ExpirationDate.encode("utf-8"),
            TraderID.encode("utf-8"),
            RejectReason,
            SendingTime,
            TradingSessionID,
            Key,
            DisplaySize,
            RefreshSize,
            Layers,
            SizeIncrement,
            PriceIncrement,
            PriceOffset,
            BOOrigPrice,
            ExecPrice,
            MsgSeqNum,
            TakeProfitPrice,
            TriggerType,
            Attributes.encode("utf-8"),
        )

    def encode_binary_string(self):
        try:
            s = struct.Struct(
                "= 1s 1s H H H I Q H H H d H d H d 12s Q d Q d d d 12s 6s H Q i i d d h d d d d d q d H 12s"
            )
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded New Limit Order message", self.binary_data, "")
            return True
        except Exception as e:
            print(e)
            return False

    def decode_binary_string(self, data):
        try:
            s = struct.Struct(
                "= 1s 1s H H H I Q H H H d H d H d 12s Q d Q d d d 12s 6s H Q i i d d h d d d d d q d H 12s"
            )
            unpacked_data = s.unpack(data)
            print("Decoded New Limit Order message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            print(e)
            return False

    def parse_header(self, data):
        return True

    def parse_message(self, data):
        self.encode_binary_string()
        return True
