"""
base message class
"""
from constant import reject_code, message_type, order_type
import json


class Message:
	def __init__(self):
		self.send_data = {}
		self.receive_data = {}
		self.RejectReason = 0
		self.reject_reasons = {k: v for k, v in reject_code.__dict__.items() if not k.startswith('_')}

	def print_reject_reason(self):
		print("Reject Code: ", self.RejectReason)
		msg = "Reject Reason: "
		if self.RejectReason in reject_code:
			msg += 'MSG: ' + str([k for k, v in self.reject_reasons.items() if self.RejectReason == v][0])
		else:
			msg += "MSG: UNKNOWN_REJECT"
		print(msg)

	def set_msg(self, msg):
		self.receive_data = msg

	def reject_reason_msg(self, reject_reason_id):
		return [k for k, v in self.reject_reasons.items() if reject_reason_id == v][0]

	def encode(self, data: dict) -> bytes:
		return json.dumps(data).encode('utf-8').replace(b', ', b',').replace(b': ', b':')

	def decode(self, data: bytes) -> dict:
		return json.loads(data)
