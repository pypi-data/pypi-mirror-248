import uuid



class Identifier:

	def __init__(self, reference):
		# Alter the reference to
		# add a Hamming code for
		# error correction
		self.value = reference
		self.hex = f'{self.value:032x}'

	@classmethod
	def Random(self):
		n = 0
		for i in range(4):
			code = uuid.uuid4().int
			n ^= (code << (8 * i))

		n = n & 0xffffffffffffffffffffffffffffffff
		return self(n)
