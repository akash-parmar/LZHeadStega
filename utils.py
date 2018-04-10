from os import listdir
from os.path import isfile, join

if __name__ == "__main__":

	path_firstname = "data/Firstname"
	path_lastname = "data/Lastname"

	list_of_firstname = [x for x in listdir(path_firstname) if isfile(join(path_firstname, x))]
	list_of_lastname = [x for x in listdir(path_lastname) if isfile(join(path_lastname, x))]

	firstname = []
	lastname = []

	print("====Firstname extraction====")
	for file in list_of_firstname:
		print(file)
		with open(join(path_firstname, file), 'r') as infile:
			for line in infile:
				firstname.append(line.split()[0].lower())

	firstname = list(set(firstname))

	print("\n====Lastname extraction====")
	for file in list_of_lastname:
		print(file)
		with open(join(path_lastname, file), 'r') as infile:
			for line in infile:
				lastname.append(line.split()[0].lower())

	lastname = list(set(lastname))

	# append firstname to result file 
	with open("data/result_firstname", 'a') as outfile:
		outfile.write("\n".join(x for x in firstname))

	# append lastname to result file 
	with open("data/result_lastname", 'a') as outfile:
		outfile.write("\n".join(x for x in lastname))