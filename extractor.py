import re
from lzwcompressor import LZWCompressor
from lzwdecompressor import LZWDecompressor

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
		for email in emails:
			k = self.get_k_by_domain(email.split('@')[1])
			if k == 0:
				result.append(get_number_from_string(email)[0])
			else:
				secret_char = email[:k]
				for c in secret_char:
					result.append(self.dictionary[c])

				num = get_number_from_string(email)
				if len(num) > 0:
					result.append(num[0])
		return result


	def get_message(self, compressed):
		lzw = LZWDecompressor()
		return lzw.decompress(compressed)


if __name__ == "__main__":
	with open("email_generated/testing.txt", 'r') as infile:
		emails = infile.readlines()

	emails = [x.split("\n")[0] for x in emails]
	extractor = MessageExtractor("domain_mapping.txt")
	result = extractor.extract(emails)
	print("\nMessage Extracted : \n", result)

	print("\nOriginal Message :\n", extractor.get_message(result))