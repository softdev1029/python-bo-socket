from base.message_wrapper import MessageWrapper


class ClientMessageWrapper(MessageWrapper):
    def __init__(self, sel, sock, addr, msgObj):
        super(ClientMessageWrapper, self).__init__(sel, sock, addr, msgObj)
