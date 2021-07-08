from base.message_controller import MessageController


class ClientMessageController(MessageController):
    def __init__(self, sel, sock, addr, msgObj):
        super(ClientMessageController, self).__init__(sel, sock, addr, msgObj)
