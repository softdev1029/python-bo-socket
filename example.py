#!/usr/bin/env python3

import sys
import traceback

from base.connection import start_connection
from base.create_message import (
    create_message,
    MSG_CLIENT_LOGON,
)
from example_message import create_client_logon, create_client_logout

message_type = ""

if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<host> <port>")
    sys.exit(1)

host, port = sys.argv[1], int(sys.argv[2])

def onMessage(ret, reason, msg, msg_len):
    print("Received message: len=", msg_len)
    if ret is False:
        print("Failed Reason: ", reason)

sel = start_connection(host, port, onMessage)

process_state = "need_logon"

try:
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            socket_controller = key.data
            
            if process_state == "need_logon":
                socket_controller.msgObj = create_client_logon()
                socket_controller.is_send = True
                print("Sending logon message ...\n")
                process_state = "need_logout"
            elif process_state == "need_logout":
                socket_controller.msgObj = create_client_logout()
                socket_controller.is_send = True
                print("Sending logout message ...\n")
                process_state = "exit"

            try:
                socket_controller.process_events(mask)
            except Exception:
                print(
                    "main: error: exception for",
                    f"{socket_controller.addr}:\n{traceback.format_exc()}",
                )
                socket_controller.close()

        if process_state == "exit":
            break
        
        # Check for a socket being monitored to continue.
        if not sel.get_map():
            break
except KeyboardInterrupt:
    print("caught keyboard interrupt, exiting")
finally:
    sel.close()
