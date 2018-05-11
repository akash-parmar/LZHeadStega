class LZWCompressor(object):

	def __init__(self):
		self.binary = True
		self.size = 256
		self.dictionary = {chr(x) : x for x in range(self.size)}
		

	def compress(self, filename):
		try:
			with open(filename, 'rb') as infile:
				content = infile.read()
			print("Uncompressed Length = ", len(content))

			w = ""
			result = []

			for c in content:
				wc = w + chr(c)

				if wc in self.dictionary:
					w = wc
				else:
					result.append(self.dictionary[w])
					# Add wc to the dictionary.
					self.dictionary[wc] = self.size
					self.size += 1
					w = chr(c)

			# Output the code for w.
			if w:
				result.append(self.dictionary[w])
				return result

		except Exception as e:
			print("Exception Found: ", str(e))
			

if __name__ == "__main__":
	lzw = LZWCompressor()
	compressed = lzw.compress("README.MD")
	print("Compressed Length = ", len(compressed))
	print("Compressed Content = \n", compressed)