import sys
import random
from name_generator import connect_db, close_db

dictionary = {
	'0000' : ('a', 'q'),
	'0001' : ('b', 'r'),
	'0010' : ('c', 's'),
	'0011' : ('d', 't'),
	'0100' : ('e', 'u'),
	'0101' : ('f', 'v'),
	'0110' : ('g', 'w'),
	'0111' : ('h', 'x'),
	'1000' : ('i', 'y'),
	'1001' : ('j', 'z'),
	'1010' : 'k',
	'1011' : 'l',
	'1100' : 'm',
	'1101' : 'n',
	'1110' : 'o',
	'1111' : 'p'
}

domain = [
	'yahoo.com', 
	'gmail.com', 
	'outlook.com',
	'rocketmail.com',
	'msn.com',
	'hotmail.com',
	'enron.com',
	'verizon.net'
]

if __name__ == "__main__":
	filename = sys.argv[1]
	with open(filename, 'rb') as infile:
		content = infile.read()
	content = [bin(int(x))[2:].zfill(8) for x in content]
	bin_string = "".join(x for x in content)

	# cover generator
	generated_email = []
	cnx = connect_db()
	cursor = cnx.cursor()

	while len(bin_string) % 11 > 0:
		bin_string += "0"

	for i in range(0, len(bin_string), 11):
		four_bit = bin_string[i:i+4]
		seven_bit = bin_string[i+4:i+11]

		char = dictionary[four_bit]
		if isinstance(char, tuple):
			char = char[random.randrange(0,2)]
		number = int(seven_bit, 2)

		# QUERY TO DATABASE
		query = "SELECT firstname FROM firstname WHERE firstname LIKE %s"
		cursor.execute(query, (char + "%",))
		temp = cursor.fetchall()
		name = [x[0] for x in temp]

		email = ""
		while email == "" or email in generated_email:
			email = name[random.randrange(0, len(name))] + str(number) + '@' + domain[random.randrange(0, len(domain))]
		generated_email.append(email)

	print("Number email generated: ", len(generated_email))
	print("Email generated: ", generated_email)

	close_db(cnx)

	if sys.argv[2] is not None:
		with open(sys.argv[2], 'w') as outfile:
			outfile.write("\n".join(x for x in generated_email))