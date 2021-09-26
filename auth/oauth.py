import pyotp
import time
import base64

api_key = "1"
totp = pyotp.TOTP(base64.b32encode(bytearray(api_key, "ascii")).decode("utf-8"))
hotp = pyotp.HOTP(base64.b32encode(bytearray(api_key, "ascii")).decode("utf-8"))
# print("hotp=", hotp.at(0))

while True:
    # print("totp=", totp.now())
    # time.sleep(1)
    pass
