# This file is for socket thread manager.


import traceback
from _thread import *


def socket_loop(sel, process_state, aes_or_oes_key, api_key, send_callback):
    """
    It is the main function running on a socket thread.
    It makes a loop processing the recv/send infinitely inside a thread.
    """

    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            socket_controller = key.data
            socket_controller.aes_or_oes_key = aes_or_oes_key

            send_callback(socket_controller, aes_or_oes_key, api_key)

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
    sel.close()


def socket_thread(sel, process_state, aes_or_oes_key, api_key, send_callback):
    """
    It makes a new socket thread with a loop function.
    """

    start_new_thread(
        socket_loop,
        (
            sel,
            process_state,
            aes_or_oes_key,
            api_key,
            send_callback,
        ),
    )
