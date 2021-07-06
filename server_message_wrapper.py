from base.message_wrapper import MessageWrapper


class ServerMessageWrapper(MessageWrapper):
    def __init__(self, sel, sock, addr, msgObj):
        super(ServerMessageWrapper, self).__init__(sel, sock, addr, msgObj)

        self._response_created = None

    def read(self):
        self._read()

        ret = True
        while len(self._recv_buffer) > 0 and ret:
            ret = self.process_request()
        self._recv_buffer = b""

        if self.msgObj.binary_data is not None:
            self._set_selector_events_mask("w")

    def write(self):
        self._send_buffer = self.msgObj.binary_data
        self._write()
