# This file is for connecting to server.

import socket
import selectors

from base.initiator_socket_controller import InitiatorSocketController
from base.logger import log


def start_connect_to_server(
    host: str, port: int, recv_callback
) -> selectors.DefaultSelector:
    """
    Server IP address and port should be provided.
    And the callback handler processing the received message should be provided.
    """

    sel = selectors.DefaultSelector()
    addr = (host, port)
    log("Starting connection to", host, ":", port, " ...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    try:
        sock.connect_ex(addr)
    except Exception as e:
        log("Connecting to server failed", e)
        return None

    log("Successfully connected to the server.")

    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    socket_controller = InitiatorSocketController(sel, sock, addr, None, recv_callback)
    sel.register(sock, events, data=socket_controller)
    return sel
