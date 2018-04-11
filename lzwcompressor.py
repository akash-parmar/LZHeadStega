class LZWCompressor(object):
	def __init__(self, string_table):
		with open(string_table, 'r') as infile:
			content = infile.readlines()
		content = [x.split("\n")[0] for x in content]

		try:
			self.size = len(content)
			self.dictionary = {x.split("->")[0] : int(x.split("->")[1]) for x in content}
			
		except Exceptiion as e:
			print("Exception Found: ", str(e))

		print(self.dictionary)

	def compress(self, filename):
		with open(filename, 'rb') as infile:
			content = infile.read()

		w = ""
		result = []

		for byte in content:
			wc = w + chr(byte)
			if wc in self.dictionary:
				w = wc
			else:
				result.append(self.dictionary[w])
				# Add wc to the dictionary.
				self.dictionary[wc] = self.size
				self.size += 1
				w = chr(byte)

		# Output the code for w.
		if w:
			result.append(self.dictionary[w])
			return result

if __name__ == "__main__":
	lzw = LZWCompressor("string_table.txt")