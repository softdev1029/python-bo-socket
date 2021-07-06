from base.message_wrapper import MessageWrapper


class ClientMessageWrapper(MessageWrapper):
    def __init__(self, sel, sock, addr, msgObj):
        super(ClientMessageWrapper, self).__init__(sel, sock, addr, msgObj)

    def read(self):
        self._read()

        ret = True
        while len(self._recv_buffer) > 0 and ret:
            ret = self.process_request()
        self._recv_buffer = b""
