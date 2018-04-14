class LZWDecompressor(object):

	def __init__(self, string_table):
		if string_table is None:
			print("Please specify the string table for LZW !")
			return

		try:
			with open(string_table, 'r') as infile:
				content = infile.readlines()
			content = [x.split("\n")[0] for x in content]

			self.size = len(content)
			self.dictionary = {int(x.split("->")[1]) : x.split("->")[0] for x in content}

			# manually add newline and tab character
			self.dictionary[self.size] = "\n"
			self.size += 1
			self.dictionary[self.size] = "\t"
			self.size += 1

		except Exception as e:
			print("Exception Found: ", str(e))


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

	compressor = LZWCompressor("string_table.txt")
	compressed = compressor.compress("README.md")
	print("\nCompressed Content :\n", compressed)

	decompressor = LZWDecompressor("string_table.txt")
	decompressed = decompressor.decompress(compressed)
	print("\nDecompressed Content :\n", decompressed)