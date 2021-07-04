import struct
from utils.helper import print_bytes_hex
from base.message import Message


class NewLimitOrder(Message):
    def __init__(self):
        self.data = ()
        self.binary_data = None

    # 40 args
    def set_parsed_data(self, *args):
        i = 0
        self.Data1 = args[i]
        i += 1
        self.Data2 = args[i]
        i += 1
        self.Data3 = args[i]
        i += 1
        self.MessageType = args[i]
        i += 1
        self.Padding = args[i]
        i += 1
        self.Account = args[i]
        i += 1
        self.OrderID = args[i]
        i += 1
        self.SymbolEnum = args[i]
        i += 1
        self.OrderType = args[i]
        i += 1
        self.SymbolType = args[i]
        i += 1
        self.BOPrice = args[i]
        i += 1
        self.BOSide = args[i]
        i += 1
        self.BOOrderQty = args[i]
        i += 1
        self.TIF = args[i]
        i += 1
        self.StopLimitPrice = args[i]
        i += 1
        self.BOSymbol = args[i]
        i += 1
        self.OrigOrderID = args[i]
        i += 1
        self.BOCancelShares = args[i]
        i += 1
        self.ExecID = args[i]
        i += 1
        self.ExecShares = args[i]
        i += 1
        self.RemainingQuantity = args[i]
        i += 1
        self.ExecFee = args[i]
        i += 1
        self.ExpirationDate = args[i]
        i += 1
        self.TraderID = args[i]
        i += 1
        self.RejectReason = args[i]
        i += 1
        self.SendingTime = args[i]
        i += 1
        self.TradingSessionID = args[i]
        i += 1
        self.Key = args[i]
        i += 1
        self.DisplaySize = args[i]
        i += 1
        self.RefreshSize = args[i]
        i += 1
        self.Layers = args[i]
        i += 1
        self.SizeIncrement = args[i]
        i += 1
        self.PriceIncrement = args[i]
        i += 1
        self.PriceOffset = args[i]
        i += 1
        self.BOOrigPrice = args[i]
        i += 1
        self.ExecPrice = args[i]
        i += 1
        self.MsgSeqNum = args[i]
        i += 1
        self.TakeProfitPrice = args[i]
        i += 1
        self.TriggerType = args[i]
        i += 1
        self.Attributes = args[i]

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
            self.set_parsed_data(
                unpacked_data[0],
                unpacked_data[1],
                unpacked_data[2],
                unpacked_data[3],
                unpacked_data[4],
                unpacked_data[5],
                unpacked_data[6],
                unpacked_data[7],
                unpacked_data[8],
                unpacked_data[9],
                unpacked_data[10],
                unpacked_data[11],
                unpacked_data[12],
                unpacked_data[13],
                unpacked_data[14],
                unpacked_data[15],
                unpacked_data[16],
                unpacked_data[17],
                unpacked_data[18],
                unpacked_data[19],
                unpacked_data[20],
                unpacked_data[21],
                unpacked_data[22],
                unpacked_data[23],
                unpacked_data[24],
                unpacked_data[25],
                unpacked_data[26],
                unpacked_data[27],
                unpacked_data[28],
                unpacked_data[29],
                unpacked_data[30],
                unpacked_data[31],
                unpacked_data[32],
                unpacked_data[33],
                unpacked_data[34],
                unpacked_data[35],
                unpacked_data[36],
                unpacked_data[37],
                unpacked_data[38],
                unpacked_data[39],
            )
            print(
                "Decoded New Limit Order message",
                "\n\tData1\t\t\t",
                self.Data1,
                "\n\tMessageLength\t\t\t",
                self.Data3,
                "\n\tMessageType\t\t",
                self.MessageType,
                "\n\tAccount\t\t\t",
                self.Account,
                "\n\tOrderID\t\t\t",
                self.OrderID,
                "\n\tSymbolEnum\t\t",
                self.SymbolEnum,
            )

            is_valid = self.validate()
            print("Valid:", is_valid)
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
