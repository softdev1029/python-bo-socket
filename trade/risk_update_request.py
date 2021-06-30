import struct
from utils.helper import print_bytes_hex
from base.message import Message


class RiskUpdateRequest(Message):
    def __init__(self):
        self.data = ()
        self.binary_data = None

    def set_data(
        self,
        data1,
        data2,
        data3,
        messageType,
        responseType,
        account,
        tradingSessionID,
        symbolEnum,
        key,
        msgSeqNum,
        sendingTime,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            messageType,
            responseType,
            account,
            tradingSessionID,
            symbolEnum,
            key,
            msgSeqNum,
            sendingTime,
        )

    def encode_binary_string(self):
        try:
            s = struct.Struct("= 1s 1s H H H I I H I I Q")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded Risk Update Request message", self.binary_data, "")
            return True
        except Exception as e:
            print(e)
            return False

    def decode_binary_string(self, data):
        try:
            s = struct.Struct("= 1s 1s H H H I I H I I Q")
            unpacked_data = s.unpack(data)
            print("Decoded Risk Update Request message", unpacked_data)
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
