from base.create_message import create_message, get_message_type_from_header
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
        header = self.parse_header(data)
        self.msgObj = create_message(get_message_type_from_header(header))

        ret = self.msgObj.parse_message(data)
        if not ret:
            print("Not parse message")
        else:
            self._recv_buffer = b""
        # if self.msgObj.binary_data is not None:
        #     self._set_selector_events_mask("w")
