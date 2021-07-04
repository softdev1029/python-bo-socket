import selectors
import struct
from base.message_wrapper import MessageWrapper


class ServerMessageWrapper(MessageWrapper):
    def __init__(self, sel, sock, addr, msgObj):
        super(ServerMessageWrapper, self).__init__(sel, sock, addr, msgObj)

        self._response_created = None

    def read(self):
        self._read()

        self.process_request()

    def write(self):
        if self._send_buffer is None:
            self._send_buffer = self.msgObj.binary_data
            self._write()

    def process_request(self):
        data = self._recv_buffer
        if self.msgObj.parse_header(data):
            ret = self.msgObj.parse_message(data)
            if not ret:
                print("Not parse message")
            if self.msgObj.binary_data is not None:
                self._set_selector_events_mask("w")
        else:
            print("Not parse header")
