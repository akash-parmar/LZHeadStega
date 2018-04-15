import smtplib
import email
import os
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE
from email.mime.base import MIMEBase
from email.parser import Parser
from email.mime.text import MIMEText
import mimetypes

class EmailSender(object):
	def __init__(self, host, port):
		self.server = smtplib.SMTP()
		self.server.connect(host,port)
		self.server.ehlo()
		self.server.starttls()

	def send(self, username, password, toaddr, subject, body):
		try:
			self.server.login(username, password)
			msg = MIMEMultipart()
			msg['From'] = username
			msg['To'] = COMMASPACE.join(toaddr)
			msg['Subject'] = subject  
			msg.attach(MIMEText(body))
			msg.attach(MIMEText('\nsent via python', 'plain'))
			self.server.sendmail(username,toaddr,msg.as_string())

			return "Email Sent Succesfully..."
		except Exception as e:
			return "Exception Found: " + str(e)


if __name__ == "__main__":
	host = 'smtp.gmail.com'
	port = 587
	sender = EmailSender(host, port)

	username = ""
	password = ""
	tolist = ["tooo1@msn.com", "abas@gmail.com", "mujahidin45@yahoo.com"]
	print(sender.send(username, password, tolist, "testing", "Test Message"))