from base.socket_controller import SocketController


class InitiatorSocketController(SocketController):
    def __init__(self, sel, sock, addr, msgObj):
        super(InitiatorSocketController, self).__init__(sel, sock, addr, msgObj)
