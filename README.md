## Create a new message

`create_message` function requies `message_type` parameter.

```
from base.create_message import (
    create_message,
    MESSAGE_TYPES,
)

message_type = MSG_CLIENT_LOGON
create_message(message_type)
```

## Socket Controller

`SocketController` requires the following parameters:

- selector: the instance of Python high-level and efficient I/O multiplexer
- sock: the instance of socket
- addr: the tuple value including host and port
- msgObj: the instance of message

```
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = (host, port)
    msgObj = create_message(message_type)
    socket_controller = SocketController(
        sel, sock, addr, msgObj
    )
```
