# Example application using the python library

The library provides the example server and client instance using the library functions.
The server runs as follows.

```
python3 server.py 0.0.0.0 4444
listening on ('0.0.0.0', 4444)
```

The client runs as follows.

```
python3 client.py 127.0.0.1 4444

starting connection to ('127.0.0.1', 4444)  ...

0       Go To Receive Mode
H       client_logon
Y       instrument_request
w       risk_update_request
E       open_order_request
f       collateral_request
T       new_limit_order

Enter a valid message type:
```

If the user selects one of message types:

```
Encoded Client Logon message 48008F0001005C890100314636410000424F55370000FA010000310000000000000000000000000000000000000000000000310000000000000000000000000000000000000000000000310000000000000000000000000000000000000000000000310000000000000000000000000000000000000000000000000000000000000029E41600439906000000000000

sending 143 bytes to ('127.0.0.1', 4444)  ...
```

Then the server displays like below:

```
Message type is client_logon
Buffer size is 143 required len is 143
Decoded Client Logon message:
        data1                            b'H'
        data2                            b'\x00'
        data3                            143
        logonType                        1
        account                          100700
        twoFA                            b'1F6A\x00\x00'
        userName                         b'BOU7\x00\x00'
        tradingSessionID                 506
        primaryOrderEntryIP              b'1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        secondaryOrderEntryIP            b'1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        primaryMarketDataIP              b'1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        secondaryMarketDataIP            b'1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        sendingTime                      0
        lastSeqNum                       1500201
        key                              432451
        loginStatus                      0
        rejectReason                     0
        riskMaster                       b'\x00'
No more receive data
```

# Library functions

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

## Process message

`process_message` requires `byte_buffer` parameter.

```
process_message(byte_buffer)
```

- RECV_NO_ERROR: the message is correct
- RECV_ERROR_NOT_ENOUGH_HEADER: the header length is not enough
- RECV_ERROR_NOT_ENOUGH_BODY: the length indicated in the header is different from the buffer length
- RECV_ERROR_INVALID_MSG_TYPE: the message type is invalid
- RECV_ERROR_PARSE: the parsing error happens

# Note

- The user is responsible for the destruction of the message.
