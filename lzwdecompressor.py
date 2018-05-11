class LZWDecompressor(object):

	def __init__(self):
		self.binary = True
		self.size = 256
		self.dictionary = {x : chr(x) for x in range(self.size)}


	def decompress(self, compressed):
		"""Decompress a list of output ks to a string."""
		from io import StringIO

		result = StringIO()
		w = self.dictionary[compressed.pop(0)]
		result.write(w)
		for k in compressed:
			if k in self.dictionary:
				entry = self.dictionary[k]
			elif k == self.size:
				entry = w + w[0]
			else:
				raise ValueError('Bad compressed k: %s' % k)
			result.write(entry)

			# Add w+entry[0] to the dictionary.
			self.dictionary[self.size] = w + entry[0]
			self.size += 1
			w = entry

		return result.getvalue()


if __name__ == "__main__":
	from lzwcompressor import LZWCompressor

	compressor = LZWCompressor()
	compressed = compressor.compress("README.md")
	print("\nCompressed Content :\n", compressed)

	decompressor = LZWDecompressor()
	decompressed = decompressor.decompress(compressed)
	print("\nDecompressed Content :\n", decompressed)