import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class CollateralRequest(Message):
    def __init__(self):
        super(CollateralRequest, self).__init__()
        self.data = ()
        self.binary_data = None

    def set_data(
        self,
        msgType1,
        msgType2,
        length,
        messageType,
        updateType,
        account,
        tradingSessionID,
        symbolEnum,
        key,
        msgSeqNum,
        sendingTime,
    ):
        self.data = (
            msgType1.encode("utf-8"),
            msgType2.encode("utf-8"),
            length,
            messageType,
            updateType,
            account,
            tradingSessionID,
            symbolEnum,
            key,
            msgSeqNum,
            sendingTime,
        )

    def encode(self):
        try:
            s = struct.Struct("= 1s 1s H H H I I H I I Q")
            self.binary_data = s.pack(*(self.data))
            print_bytes_hex("Encoded Collateral Req message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)


def create_example_collateral_request():
    message = CollateralRequest()
    message.set_data("f", "", 34, 0, 0, 100500, 0, 1, 0, 0, 1623152815)

    return message
