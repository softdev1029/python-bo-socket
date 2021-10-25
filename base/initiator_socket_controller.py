"""
This file is for creating the socket controller of initiator.
Initiator is responsible for listening and acceptance of client sockets.
"""

from base.socket_controller import SocketController


class InitiatorSocketController(SocketController):
    def __init__(self, sel, sock, addr, msgObj, recv_callback):
        super(InitiatorSocketController, self).__init__(
            sel, sock, addr, msgObj, recv_callback
        )
