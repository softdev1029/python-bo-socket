import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class MDSubscribe(Message):
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
        key,
        tradingSessionID,
        sendTime,
        seqNum,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            messageType,
            padding,
            account,
            key,
            tradingSessionID,
            sendTime,
            seqNum,
        )

    def encode(self):
        try:
            s = struct.Struct("= 1s 1s H H H I I I q I")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded MD Subscribe message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def decode(self, data):
        try:
            s = struct.Struct("= 1s 1s H H H I I I q I")
            unpacked_data = s.unpack(data)
            log("Decoded MD Subscribe message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)


def create_md_subscribe():
    message = MDSubscribe()
    message.set_data(
        "s",  # data1
        "",  # data2
        32,  # data3
        1,  # MessageType, TOB
        0,  # padding
        100700,  # account
        468321,  # key
        200,  # tradingSessionID
        184232029271,  # sendTime
        52488131,  # seqNum
    )
    return message
