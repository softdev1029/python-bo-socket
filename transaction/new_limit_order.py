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

    def encode(self):
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

    def decode(self, data):
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
        self.decode(data)
        return True


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
    return message
