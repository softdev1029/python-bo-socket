from base.message_wrapper import MessageWrapper


class ClientMessageWrapper(MessageWrapper):
    def __init__(self, sel, sock, addr, msgObj):
        super(ClientMessageWrapper, self).__init__(sel, sock, addr, msgObj)

    def read(self):
        need_read = True

        while need_read:
            recv_len = self._read()

            need_read = recv_len > 0

            ret = True
            while ret:
                (ret, reason) = self.process_request()

        # here, _recv_buffer should be empty
        # otherwise, we need to check reason
