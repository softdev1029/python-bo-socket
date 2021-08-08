import struct
from utils.helper import print_bytes_hex
from base.message import Message
from base.logger import log


class BaseLevelData(Message):
    def __init__(self):
        self.data = ()
        self.binary_data = None

    def encode(self):
        try:
            format = "= 1s 1s H H H H H q I H 12s"
            for i in range(self.level_count):
                format += " d d B"
            s = struct.Struct(format)
            self.binary_data = s.pack(*(self.data))
            log(self.level_count / 2, "Level ...")
            print_bytes_hex("Encoded Level Data message", self.binary_data, "")
            return True
        except Exception as e:
            log(e)
            return False

    def decode(self, data):
        try:
            format = "= 1s 1s H H H H H q I H 12s"
            for i in range(self.level_count):
                format += " d d B"
            s = struct.Struct(format)
            unpacked_data = s.unpack(data)
            log(self.level_count / 2, "Level ...")
            log("Decoded Level Data message", unpacked_data)
            self.binary_data = data
            return True
        except Exception as e:
            log(e)
            return False

    def parse_message(self, data):
        return self.decode(data)
