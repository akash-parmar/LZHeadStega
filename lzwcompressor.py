class LZWCompressor(object):

	def __init__(self, string_table):
		if string_table is None:
			print("Please specify the string table for LZW !")
			return

		try:
			with open(string_table, 'r') as infile:
				content = infile.readlines()
			content = [x.split("\n")[0] for x in content]

			self.size = len(content)
			self.dictionary = {x.split("->")[0] : int(x.split("->")[1]) for x in content}

			# manually add newline and tab character
			self.dictionary['\n'] = self.size
			self.size += 1
			self.dictionary['\t'] = self.size
			self.size += 1

		except Exception as e:
			print("Exception Found: ", str(e))


	def compress(self, filename):

		try:
			with open(filename, 'r') as infile:
				content = infile.read()
			print("Uncompressed Length = ", len(content))

			w = ""
			result = []

			for c in content:
				wc = w + c

				if wc in self.dictionary:
					w = wc
				else:
					result.append(self.dictionary[w])
					# Add wc to the dictionary.
					self.dictionary[wc] = self.size
					self.size += 1
					w = c

			# Output the code for w.
			if w:
				result.append(self.dictionary[w])
				return result

		except Exception as e:
			print("Exception Found: ", str(e))
			

if __name__ == "__main__":
	lzw = LZWCompressor("string_table.txt")
	compressed = lzw.compress("README.MD")
	print("Compressed Length = ", len(compressed))
	print("Compressed Content = \n", compressed)