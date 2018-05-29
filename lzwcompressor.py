class LZWCompressor(object):

	def __init__(self, filename):
		try:
			with open(filename, 'r') as infile:
				content = infile.read()
			content = content.split('\n')

			self.size = len(content)
			self.dictionary = {chr(int(x.split('->')[0])) : int(x.split('->')[1]) for x in content}

		except Exception as e:
			print("Exception Found: ", str(e))


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
	lzw = LZWCompressor('string_table')
	compressed = lzw.compress("README.MD")
	print("Compressed Length = ", len(compressed))
	print("Compressed Content = \n", compressed)