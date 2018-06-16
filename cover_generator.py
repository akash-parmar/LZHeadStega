from lzwcompressor import LZWCompressor
from name_generator import connect_db, close_db
from headstega import dictionary as coverdictionary
import random

def check_alphabet_lower(s):
	if len(s) > 1:
		return False

	if ord(s) < 97 or ord(s) > 122:
		return False
	return True


def query_database_name(cnx, s):
	cursor = cnx.cursor()
	query1 = "SELECT lastname FROM lastname WHERE lastname LIKE %s ORDER BY UUID() LIMIT 100"
	cursor.execute(query1, (s + "%",))
	temp = cursor.fetchall()
	name1 = [x[0] for x in temp]

	query2 = "SELECT firstname FROM firstname WHERE firstname LIKE %s ORDER BY UUID() LIMIT 100"
	cursor.execute(query2, (s + "%",))
	temp = cursor.fetchall()
	name2 = [x[0] for x in temp]

	return list(set(name1 + name2))


def query_database_random(cnx):
	cursor = cnx.cursor()
	query = "SELECT lastname FROM lastname WHERE RAND() <= 0.0005 LIMIT 1"
	cursor.execute(query)
	name = cursor.fetchone()
	return name[0]


def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1]
    return li_dif


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
		message_bit = [bin(int(x))[2:].zfill(8) for x in message]
		print(message_bit)
		cnx = connect_db()
		generated_email = []
		generated_name = []
		i = 0
		half = False

		while i < len(message_bit):
			if len(message_bit[i]) > 8:
				# larger than 256, so we generate random email and add the information as a number in email username
				name = query_database_random(cnx)
				while name in generated_name:
					name = query_database_random(cnx)

				generated_name.append(name)
				email = name + str(int(message_bit[i], 2)) + '@' + self.domain_map[0]
				generated_email.append(email)
				i += 1
			else:
				# smaller than 256 so we continue to append until database cannot give us a valid name
				if not half:
					word = coverdictionary[message_bit[i][:4]]
				else:
					word = coverdictionary[message_bit[i][4:]]

				if isinstance(word, tuple):
					word = word[random.randrange(0,2)]
				name = query_database_name(cnx, word)
				name = Diff(generated_name, name)

				if len(name) > 0:
					temp_name = name
					half = not half
					if not half:
						i += 1

					while i < len(message_bit) and len(word) < len(self.domain_map):
						if len(message_bit[i]) <= 8:
							if half:
								temp = coverdictionary[message_bit[i][4:]]
								if isinstance(temp, tuple):
									temp = temp[random.randrange(0,2)]
								word += temp
							else:
								temp = coverdictionary[message_bit[i][:4]]
								if isinstance(temp, tuple):
									temp = temp[random.randrange(0,2)]
								word += temp

							name = query_database_name(cnx, word)
							name = Diff(generated_name, name)
							if len(name) > 0:
								half = not half
								temp_name = name
								if not half:
									i += 1
							else:
								word = word[:-1]
								break
						else:
							break
					username = temp_name[random.randrange(0, len(temp_name))]
					generated_name.append(username)

					if not half and i < len(message_bit):
						email = username + str(int(message_bit[i], 2)) + '@' + self.domain_map[len(word)]
						i += 1
					else: 
						email = username + '@' + self.domain_map[len(word)]
					generated_email.append(email)
				else:
					username = query_database_random(cnx)
					generated_name.append(username)
					if not half:
						email = username + str(int(message_bit[i][:4], 2)) + '@' + self.domain_map[0]
					else:
						email = username + str(int(message_bit[i][4:], 2)) + '@' + self.domain_map[0]
						i += 1
					half = not half
					generated_email.append(email)

		close_db(cnx)
		return generated_email


if __name__ == "__main__":
	lzw = LZWCompressor('string_table')
	compresed = lzw.compress("input_txt/paper.txt")
	print("Compressed Length = ", len(compresed))
	print("Compressed Content = \n", compresed)

	generator = CoverGenerator("domain_mapping", lzw.dictionary)
	#print("\nstring table : \n", generator.dictionary)
	#print("\ndomain mapping : \n", generator.domain_map)
	result = generator.generate_cover(compresed)
	print("\nTotal Email : \n", len(result))
	print("\nEmail Generated : \n", result)

	with open("email_generated/testing.txt", 'w') as outfile:
		outfile.write("\n".join(x for x in result))