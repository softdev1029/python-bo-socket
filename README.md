# API Doc Link

http://api.crmd.bo.market:4568

# Install

pip install -r requirements.txt

# Example application using the python library

The library provides the example server and client instance using the library functions.
The AES server runs as follows.

```
python3 example_server_aes.py 0.0.0.0 4444
listening on ('0.0.0.0', 4444)
```

Then, the OES server runs as follows.

```
python3 example_server_oes.py 0.0.0.0 4445
listening on ('0.0.0.0', 4444)
```

The client runs as follows.

```
python3 example_client.py 127.0.0.1 4444
```

First, you should input API Trading Key, User Name and Account.

```
Enter API Trading Key: 1
Enter User Name: 1
Enter Account: 1
```

Then, it successfully connects to the AES server.

```
[lib]  The AES server is 127.0.0.1 : 4444

[lib]  Starting connection to 127.0.0.1 : 4444  ...
[lib]  Successfully connected to the server.
```

And it sends the AES Logon message.

```
[lib]  Send the AES Logon message

[lib]  Encoded Client Logon message 48008F00010001000000353137383436310000000000FA010000310000000000000000000000000000000000000000000000310000000000000000000000000000000000000000000000310000000000000000000000000000000000000000000000310000000000000000000000000000000000000000000000000000000000000029E41600000000000000000000
[lib]  Sending 143 bytes to 127.0.0.1 : 4444  ..
```

The AES server replies with the OES server IP and Port.

```
[lib]  Read 143 bytes from 127.0.0.1 : 4444

[lib]  Processing the received message ...
[lib]  Message type is client_logon
[lib]  Buffer size is 143 required len is 143
[lib]    Data1 :  H
[lib]    Data2 :
[lib]    Data3 :  143
[lib]    LogonType :  1
[lib]    Account :  100700
[lib]    TwoFA :  1F6A
[lib]    UserName :  BOU7
[lib]    TradingSessionID :  506
[lib]    PrimaryOrderEntryIP :  127.0.0.1:4445
[lib]    SecondaryOrderEntryIP :  1
[lib]    PrimaryMarketDataIP :  1
[lib]    SecondaryMarketDataIP :  1
[lib]    SendingTime :  0
[lib]    LastSeqNum :  1500201
[lib]    Key :  432451
[lib]    LoginStatus :  1
[lib]    RejectReason :  0
[lib]    RiskMaster :
[lib]  Valid: True
```

After getting the information of the OES server, it connects to the OES server.

```
[lib]  From AES server, Received message: len= 143
[lib]  AES Logon success
[lib]  The OES server is 127.0.0.1 : 4445
[lib]  Starting connection to 127.0.0.1 : 4445  ...
[lib]  Successfully connected to the server.
```

Then, the client sends the OES Logon message.

```
[lib]  Read 143 bytes from 127.0.0.1 : 4444

[lib]  At send_callback to OES ...
[lib]  Processing the received message ...
[lib]  Send the OES Logon message
```

The library always updates Tx/Rx counter.

```
[lib]  At sending, Message Counter is 0 Tx/Rx state is recv_logon
```

Every 1 second, the client sends the Transaction message with a different Message Type and a different Order Type.

```
[lib]  At send_callback to OES ...
[lib]  Sending the Order message, msg_type= 1 order_type= 1
```

# the 2nd Example application using the python library

The library provides the example server and client instance using the library functions.
The server runs as follows.

```
python3 example_server.py 0.0.0.0 4444
listening on ('0.0.0.0', 4444)
```

The client runs as follows.

```
python3 example_client.py 127.0.0.1 4444

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

The current `server.py` replies `logon` message as example.
You can change it to other message in `ResponserSocketController.process_state`.

In `example_client.py`, to receive the server message, select `0: Go To Receive Mode`.

# Another example application using the python library

Another example of client is defined in `example_client2.py`.
This client example emulates the whole flow including logon.

## Input the necessary information

As the first step, you should input the server IP address and port number.
You need to input the API Trading Key, too.

```
1. Specify the IPv4 address and the port number of the server

Enter a valid IPv4 address: 127.0.0.1
Enter a valid port number: 4444
[lib]  Starting connection to ('127.0.0.1', 4444)  ...
[lib]  Successfully connected to the server.
Enter API Trading Key: 1
```

## Send Logon message

As the second step, it tries to logon.
The client sends `logon` message.
And the server replies `logon`, too.

And the client sends `New Order` message.
The server replies `Order Reply` message.

# Library functions

## Create a new message

`create_example_message` function requies `message_type` parameter.

```
from base.create_example_message import (
    create_example_message,
    MESSAGE_TYPES,
)

message_type = MSG_CLIENT_LOGON
create_example_message(message_type)
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
    msgObj = create_example_message(message_type)
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
