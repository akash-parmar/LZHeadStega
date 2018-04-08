import mysql.connector
from mysql.connector import errorcode
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

def generate_fake_male(n=100):
	fake = Faker()
	result = [fake.name_male() for i in range(n)]
	return result


if __name__ == "__main__" :
	cnx = connect_db()
	close_db(cnx)