class Message:
    def __init__(self):
        pass

    def set_data(self, *args):
        pass

    def encode_binary_string(self):
        return False

    def decode_binary_string(self, data):
        return False

    def parse_header(self, data):
        return True

    def parse_message(self, data):
        return True
