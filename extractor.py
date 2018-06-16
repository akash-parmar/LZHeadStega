import re
from lzwcompressor import LZWCompressor
from lzwdecompressor import LZWDecompressor
from headstega_extractor import dictionary as extractdictionary

def get_number_from_string(s):
	result = re.findall('\d+', s)
	result = [int(x) for x in result]
	return result

class MessageExtractor(object):
	def __init__(self, domain_mapping):
		if domain_mapping is None:
			print("Please Specify the domain mapping !")
			return

		try:
			# read domain mapping
			with open(domain_mapping, 'r') as infile:
				content = infile.readlines()
			self.domain_map = {x : content[x].split("\n")[0] for x in range(len(content))}

			# read string table
			self.size = 256
			self.dictionary = {chr(x) : x for x in range(self.size)}

		except Exception as e:
			print("Exception Found: ", str(e))


	def get_k_by_domain(self, value):
		return list(self.domain_map.keys())[list(self.domain_map.values()).index(value)]


	def extract(self, emails):
		result = []
		binstring = ['00000000']
		for email in emails:
			k = self.get_k_by_domain(email.split('@')[1])
			if k == 0:
				num = get_number_from_string(email)[0]
				if num <= 15:
					if len(binstring[-1]) <= 8:
						binstring[-1] = binstring[-1] + bin(num)[2:].zfill(4)
					else:
						binstring.append(bin(num)[2:].zfill(4))
				else:
					binstring.append(bin(num)[2:])
			else:
				secret_char = email[:k]
				for c in secret_char:
					if len(binstring[-1]) < 8:
						binstring[-1] = binstring[-1] + extractdictionary[c]
					else:
						binstring.append(extractdictionary[c])

				num = get_number_from_string(email)
				if len(num) > 0:
					num = num[0]
					if num <= 255:
						binstring.append(bin(num)[2:].zfill(8))
					else:
						binstring.append(bin(num)[2:])

		# Remove the padding in the front and extract the message
		binstring = binstring[1:]
		result = [int(x,2) for x in binstring]
		print("extracted: ", result)
		return result


	def get_message(self, compressed, string_table_path):
		lzw = LZWDecompressor(string_table_path)
		return lzw.decompress(compressed)


if __name__ == "__main__":
	with open("email_generated/testing.txt", 'r') as infile:
		emails = infile.readlines()

	emails = [x.split("\n")[0] for x in emails]
	extractor = MessageExtractor("domain_mapping")
	result = extractor.extract(emails)
	print("\nMessage Extracted : \n", result)

	print("\nOriginal Message :\n", extractor.get_message(result, 'string_table'))