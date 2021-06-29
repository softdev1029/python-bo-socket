# Byte list prints data in hexadecimal format
def print_bytes_hex(desc, data, delimiter):
    lin = ["%02X" % i for i in data]
    print(desc, delimiter.join(lin))
