import struct
from utils.helper import print_bytes_hex
from base.message import Message


class OpenOrderRequest(Message):
    def __init__(self):
        self.data = ()
        self.binary_data = None

    def set_data(
        self,
        data1,
        data2,
        data3,
        messageType,
        Account,
        SymbolEnum,
        SymbolName,
        TradingSessionID,
        SendingTime,
        MsgSeqNum,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            messageType,
            Account,
            SymbolEnum,
            SymbolName.encode("utf-8"),
            TradingSessionID,
            SendingTime,
            MsgSeqNum,
        )

    def encode_binary_string(self):
        try:
            s = struct.Struct("= 1s 1s h h i h 12s i q i")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded Open Order Request message", self.binary_data, "")
            return True
        except Exception as e:
            print(e)
            return False

    def decode_binary_string(self, data):
        try:
            s = struct.Struct("= 1s 1s h h i h 12s i q i")
            unpacked_data = s.unpack(data)
            print("Decoded Open Order Request message", unpacked_data)
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
