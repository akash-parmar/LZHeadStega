from lzwcompressor import LZWCompressor
from name_generator import connect_db, close_db

def check_alphabet_lower(s):
	if len(s) > 1:
		return False

	if ord(s) < 97 or ord(s) > 122:
		return False
	return True

class CoverGenerator(object):
	def __init__(self, domain_mapping, string_table):
		'''
		@param string_table is an lzw dictionary object, not a path
		'''

		if domain_mapping is None or string_table is None:
			print("Please Specify the domain mapping and string table !")
			return

		try:
			# read domain mapping
			with open(domain_mapping, 'r') as infile:
				content = infile.readlines()
			self.domain_map = {x : content[x].split("\n")[0] for x in range(len(content))}

			# read string table
			self.dictionary = string_table
			self.size = len(self.dictionary)

		except Exception as e:
			print("Exception Found: ", str(e))


	def get_key_by_value(self, value):
		return list(self.dictionary.keys())[list(self.dictionary.values()).index(value)]


	def generate_cover(self, message):
		cnx = connect_db()
		cursor = cnx.cursor()
		i = 0
		generated_email = []

		while i < len(message):
			j = i
			word = []
			word_string = ""

			while check_alphabet_lower(self.get_key_by_value(message[j])) and len(word_string) < len(self.domain_map):
				word.append(message[j])
				word_string = "".join(self.get_key_by_value(x) for x in word)
				j += 1
				if j >= len(message):
					break

			# query the database, j is the index of non alphabet char
			if len(word) == 0:
				email = ""

				while len(email) == 0 or email in generated_email:
					# first char is non alphabet
					query = "SELECT lastname FROM lastname WHERE RAND() <= 0.0005 LIMIT 1"
					cursor.execute(query)
					name = cursor.fetchone()
					email = name[0] + str(message[j]) + "@" + self.domain_map[0]
				generated_email.append(email)
				i += 1

			else:
				word.append(0) # dummy
				j += 1 # dummy
				email = ""
				name = []
				
				# query the database, search for names that contains word
				while len(name) == 0 and len(word) > 0:
					word.pop()
					j -= 1
					query1 = "SELECT lastname FROM lastname WHERE lastname LIKE %s"
					word_string = "".join(self.get_key_by_value(x) for x in word)
					cursor.execute(query1, (word_string + "%",))
					temp = cursor.fetchall()
					temp = [x[0] for x in temp]
					name += temp

					if len(name) == 0:
						query2 = "SELECT firstname FROM firstname WHERE firstname LIKE %s"
						cursor.execute(query2, (word_string + "%",))
						temp = cursor.fetchall()
						temp = [x[0] for x in temp]
						name += temp

				# if still no result in db, treat message[j] as a non alphabet
				if len(word) == 0:
					while len(email) == 0 or email in generated_email:
						# first char is non alphabet
						query = "SELECT lastname FROM lastname WHERE RAND() <= 0.000005 LIMIT 1"
						cursor.execute(query)
						name = cursor.fetchone()
						email = name[0] + str(message[j]) + "@" + self.domain_map[0]
					generated_email.append(email)
					i += 1
				else :
					for _ in name:
						if j < len(message):
							if check_alphabet_lower(self.get_key_by_value(message[j])):
								# stop appending message into word because len(word_string) == len(self.domain_map)
								email = _ + "@" + self.domain_map[len(word_string)]
								if email not in generated_email:
									generated_email.append(email)
									i += len(word)
									break
							else:
								# stop appending message into word because chr(message[i]) is not an alphabet
								email = _ + str(message[j]) + "@" + self.domain_map[len(word_string)]
								if email not in generated_email:
									generated_email.append(email)
									i += len(word) + 1
									break
						else:
							email = _ + "@" + self.domain_map[len(word_string)]
							if email not in generated_email:
								generated_email.append(email)
								i += len(word)
								break
		close_db(cnx)
		return generated_email


if __name__ == "__main__":
	lzw = LZWCompressor()
	compresed = lzw.compress("input_txt/sample1.txt")
	print("Compressed Length = ", len(compresed))
	print("Compressed Content = \n", compresed)

	generator = CoverGenerator("domain_mapping.txt", lzw.dictionary)
	print("\nstring table : \n", generator.dictionary)
	print("\ndomain mapping : \n", generator.domain_map)
	result = generator.generate_cover(compresed)
	print("\nTotal Email : \n", len(result))
	print("\nemail generated : \n", result)

	with open("email_generated/testing.txt", 'w') as outfile:
		outfile.write("\n".join(x for x in result))