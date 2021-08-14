#!/usr/bin/env python3

import socket
import selectors

import initiator_socket_controller
from base.logger import log

sel = selectors.DefaultSelector()

def start_connection(host, port, recv_callback):
    addr = (host, port)
    log("Starting connection to", addr, " ...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.connect_ex(addr)

    log("Successfully connected to the server.")

    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    socket_controller = initiator_socket_controller.InitiatorSocketController(
        sel, sock, addr, None, recv_callback
    )
    sel.register(sock, events, data=socket_controller)
    return sel

