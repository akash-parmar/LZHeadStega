import sys
import re

dictionary = {
	'a' : '0000', 
	'b' : '0001', 
	'c' : '0010', 
	'd' : '0011', 
	'e' : '0100', 
	'f' : '0101', 
	'g' : '0110', 
	'h' : '0111', 
	'i' : '1000', 
	'j' : '1001', 
	'k' : '1010', 
	'l' : '1011', 
	'm' : '1100', 
	'n' : '1101', 
	'o' : '1110', 
	'p' : '1111',
	'q' : '0000',
	'r' : '0001',
	's' : '0010',
	't' : '0011',
	'u' : '0100',
	'v' : '0101',
	'w' : '0110',
	'x' : '0111',
	'y' : '1000',
	'z' : '1001'
}

def get_number_from_string(s):
	result = re.findall('\d+', s)
	result = [int(x) for x in result]
	return result

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print("specify the input file!")
	else:
		filename = sys.argv[1]

	with open(filename, 'r') as infile:
		content = infile.read()
	emails = content.split("\n")

	extracted = ""
	for email in emails:
		extracted += dictionary[email[0]]
		number_part = get_number_from_string(email)
		if len(number_part) > 0:
			extracted += bin(number_part[0])[2:].zfill(7)

	result = []
	for i in range(0, len(extracted), 8):
		cur = extracted[i:i+8]
		result.append(int(cur, 2))

	result = bytes(result)
	while result[-1] == '\x00':
		result = result[:-1]

	filename = input("To view the message, you must save it\nFilename: ")
	with open(filename, 'wb') as out:
		out.write(bytes(result)[:-1])