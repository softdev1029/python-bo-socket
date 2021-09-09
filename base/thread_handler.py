import traceback
from _thread import *


def socket_loop(sel, process_state, send_callback):
    while True:
        events = sel.select(timeout=1)
        for key, mask in events:
            socket_controller = key.data

            send_callback(socket_controller)

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


def socket_thread(sel, process_state, send_callback):
    start_new_thread(
        socket_loop,
        (
            sel,
            process_state,
            send_callback,
        ),
    )
