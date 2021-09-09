import traceback


def socket_thread(sel, process_state, send_callback):
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
