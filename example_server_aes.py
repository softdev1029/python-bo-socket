# This file is for the example AES server
# It is not part of the python client library and it provides the example python server.


import sys
import socket
import selectors
import traceback

import server_aes_socket_controller


sel = selectors.DefaultSelector()


def onMessage(ret, reason, msg, msg_len):
    """
    It is the server socket's receiving callback function.
    """
    print("Received message: len=", msg_len)
    if ret is False:
        print("Failed Reason: ", reason)


def start_connection(host, port):
    """
    As server, it is listening to all client's requests for establishing the connections
    """
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Avoid bind() exception: OSError: [Errno 48] Address already in use
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind((host, port))
    lsock.listen()
    print("listening on", (host, port))
    lsock.setblocking(False)
    sel.register(lsock, selectors.EVENT_READ, data=None)


def accept_wrapper(
    sock,
):
    """
    As server, it establishes the connection by accepting the client socket's request.
    """
    conn, addr = sock.accept()  # Should be ready to read

    print("accepted connection from", addr)
    conn.setblocking(False)

    socket_controller = server_aes_socket_controller.ResponserSocketController(
        sel, conn, addr, None, onMessage
    )
    sel.register(conn, selectors.EVENT_READ, data=socket_controller)


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])
# host = "0.0.0.0"
# port = 4444

start_connection(host, port)

try:
    while True:
        events = sel.select(timeout=None)
        for key, mask in events:
            if key.data is None:
                accept_wrapper(
                    key.fileobj,
                )
            else:
                socket_controller = key.data
                try:
                    socket_controller.process_events(mask)
                except Exception:
                    print(
                        "main: error: exception for",
                        f"{socket_controller.addr}:\n{traceback.format_exc()}",
                    )
                    socket_controller.close()
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
