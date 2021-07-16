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
