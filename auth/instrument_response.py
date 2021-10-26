import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class InstrumentResponse(Message):
    def __init__(self):
        super(InstrumentResponse, self).__init__()
        self.data = ()
        self.binary_data = None

    def set_data(
        self,
        data1,
        data2,
        data3,
        messageType,
        padding,
        responseType,
        symbolEnum,
        symbolName,
        symbolType,
        priceIncrement,
        minSize,
        maxSize,
        sendingTime,
        msgSeqNum,
    ):
        self.data = (
            data1.encode("utf-8"),
            data2.encode("utf-8"),
            data3,
            messageType,
            padding,
            responseType,
            symbolEnum,
            symbolName.encode("utf-8"),
            symbolType,
            priceIncrement,
            minSize,
            maxSize,
            sendingTime,
            msgSeqNum,
        )

    def encode(self):
        try:
            s = struct.Struct("= 1s 1s H H H H H 24s H e e e Q I")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded Instrument Response message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def decode(self, data):
        try:
            s = struct.Struct("= 1s 1s H H H H H 24s H e e e Q I")
            unpacked_data = s.unpack(data)
            log("Decoded Instrument Response message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)


def create_example_instrument_response(aes_or_oes_key):
    message = InstrumentResponse()
    message.set_data(
        "Y",  # data1
        "",  # data2
        62,  # data3
        59,  # MessageType, not really required since a message of this type is defined in the first byte of the header
        0,  # Padding
        2,  # ResponseType
        1,  # SymbolEnum
        "BTCUSD",  # SymbolName
        1,  # SymbolType
        0.5,  # PriceIncrement
        0.00001,  # MinSize
        1000,  # MaxSize
        0,  # SendingTime
        1500201,  # MsgSeqNum
    )
    return message
