import mysql.connector
from mysql.connector import errorcode, Error
from faker import Faker
from config import database_config


def connect_db():
	try:
		cnx = mysql.connector.connect(**database_config)
		print("Database Established...")
		return cnx

	except mysql.connector.Error as e:
		if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			print("Something is wrong with your user name or password")
		elif err.errno == errorcode.ER_BAD_DB_ERROR:
			print("Database does not exist")
		else:
			print(err)

	return False

def close_db(cnx):
	cnx.close()
	print("Database Connection Closed...")

def extract_name_from_csv(filename):
	result = []
	with open(filename, 'r') as infile:
		for line in infile:
			result.append(line.replace("\n", "").lower())

	return list(set(result))

def save_name_to_database(cnx, data, firstname=True):
	try:
		if firstname:
			query = "INSERT IGNORE INTO firstname(firstname) VALUES (%s)"
		else:
			query = "INSERT IGNORE INTO lastname(lastname) VALUES (%s)"

		cursor = cnx.cursor()
		data = [(x,) for x in data]
		cursor.executemany(query, data)
		cnx.commit()

	except Error as e:
		print("Exception : ", str(e))

	finally:
		cursor.close()

if __name__ == "__main__" :
	cnx = connect_db()
	firstnames = extract_name_from_csv("data/Firstname.csv")
	lastnames = extract_name_from_csv("data/Lastname.csv")
	save_name_to_database(cnx, firstnames)
	save_name_to_database(cnx, lastnames, firstname=False)
	close_db(cnx)