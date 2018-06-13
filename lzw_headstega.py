from tkinter import *
from tkinter import ttk, filedialog, scrolledtext, messagebox
from functools import partial
from lzwcompressor import LZWCompressor
from lzwdecompressor import LZWDecompressor
from extractor import MessageExtractor
from cover_generator import CoverGenerator
from email_sender import EmailSender
from os.path import isfile
import time


class Window:
	def __init__(self, master):
		# initialize frame
		self.top_frame = Frame(master=master)
		self.top_frame.pack(expand=TRUE, fill=BOTH)

		self.bottom_frame = Frame(master=master)
		self.bottom_frame.pack(fill=BOTH, side=BOTTOM)

		# initialize tabbed widgets
		self.initialize_tabbed_widgets()

		# component for message Hiding
		self.initialize_message_hiding()

		# component for message extracting
		self.initialize_message_extracting()

		# Bottom_Frame
		quit_button = Button(self.bottom_frame, text='Quit', command=master.destroy)
		quit_button.pack(side=RIGHT, padx=5)


	def initialize_tabbed_widgets(self):
		self.tab_menu = ttk.Notebook(self.top_frame)

		# initialize the individual tab menu
		self.tab_email_generator = ttk.Frame(self.tab_menu)
		self.tab_email_extractor = ttk.Frame(self.tab_menu)

		# add individual tab menu into tabbed widgets
		self.tab_menu.add(self.tab_email_generator, text='Message Hiding')
		self.tab_menu.add(self.tab_email_extractor, text='Message Extraction')

		# show tabbed widgets
		self.tab_menu.pack(expand=1, fill="both")


	def initialize_message_hiding(self):
		frame_hiding = Frame(self.tab_email_generator)
		frame_hiding.place(anchor='nw', relx=0.05, rely=0.05)

		# Label
		plaintext_label = Label(frame_hiding, text="Secret Message: ")
		plaintext_label.grid(row=0, column=0, padx=5, pady=2.5)

		dictionary_label = Label(frame_hiding, text="String Table: ")
		dictionary_label.grid(row=1, column=0, padx=5, pady=2.5)

		domain_label = Label(frame_hiding, text="Domain Mapping: ")
		domain_label.grid(row=2, column=0, padx=5, pady=2.5)

		cover_result_label = Label(frame_hiding, text="Email Generated: ")
		cover_result_label.grid(row=4, column=0, padx=5, pady=5)

		# Entry
		self.hiding_plaintext_entry = Entry(frame_hiding, width=50)
		self.hiding_plaintext_entry.grid(row=0, column=1, padx=5, pady=2.5)

		self.hiding_dictionary_entry = Entry(frame_hiding, width=50)
		self.hiding_dictionary_entry.grid(row=1, column=1, padx=5, pady=2.5)

		self.hiding_domain_entry = Entry(frame_hiding, width=50)
		self.hiding_domain_entry.grid(row=2, column=1, padx=5, pady=2.5)

		# scrolled text
		self.email_generated = scrolledtext.ScrolledText(frame_hiding, width=60, height=20)
		self.email_generated.grid(row=5, column=0, padx=5, pady=2.5, columnspan=20)

		# Button
		browse_plaintext_button = Button(frame_hiding, text="Browse", command=partial(self.browse_plaintext, self.hiding_plaintext_entry))
		browse_plaintext_button.grid(row=0, column=2, padx=5, pady=2.5)

		browse_dictionary_button = Button(frame_hiding, text="Browse", command=partial(self.browse_plaintext, self.hiding_dictionary_entry))
		browse_dictionary_button.grid(row=1, column=2, padx=5, pady=2.5)

		browse_domain_button = Button(frame_hiding, text="Browse", command=partial(self.browse_plaintext, self.hiding_domain_entry))
		browse_domain_button.grid(row=2, column=2, padx=5, pady=2.5)

		generate_cover_button = Button(frame_hiding, text="Generate Cover", command=self.generate_cover)
		generate_cover_button.grid(row=3, column=0, padx=5, pady=2.5)

		send_button = Button(frame_hiding, text="Send Email", command=self.send_window)
		send_button.grid(row=6, column=0, padx=5, pady=2.5)


	def browse_plaintext(self, target):
		f = filedialog.askopenfilename(initialdir="/", title="Select file")
		if f:
			target.delete(0, END)
			target.insert(0, f)


	def generate_cover(self):
		secret_path = self.hiding_plaintext_entry.get()
		dictionary_path = self.hiding_dictionary_entry.get()
		domain_mapping = self.hiding_domain_entry.get()

		try:
			if len(secret_path) == 0 or len(domain_mapping) == 0 or len(dictionary_path) == 0:
				raise Exception("Please select the plaintext, dictionary and domain mapping !")
			if not isfile(secret_path) or not isfile(domain_mapping) or not isfile(dictionary_path):
				raise Exception("Cannot find the specified file !")

			start = time.clock()
			compressor = LZWCompressor(dictionary_path)
			compressed = compressor.compress(secret_path)
			print("len compressed: ", len(compressed))
			generator = CoverGenerator(domain_mapping, compressor.dictionary)
			result = generator.generate_cover(compressed)
			end = time.clock()

			self.email_generated.delete(1.0, END)
			self.email_generated.insert(INSERT, "\n".join(x for x in result))

			summary = "Elapsed Time: " + str(end-start) + " seconds\nTotal: " + str(len(result)) + " email\n"
			messagebox.showinfo("Summary", summary)

		except Exception as e:
			messagebox.showerror('Exception Caught', str(e))


	def send_window(self):
		window = Toplevel()
		window.title("Send Email")
		window.geometry('500x500')

		frame = Frame(window)
		frame.pack(expand=TRUE, fill=BOTH)

		bottom_frame = Frame(window)
		bottom_frame.pack(fill=BOTH, side=BOTTOM)

		#Label 
		email_host = Label(frame, text="Host")
		email_host.grid(row=0, column=0, padx=5, pady=2.5)

		email_username = Label(frame, text="Email Username")
		email_username.grid(row=1, column=0, padx=5, pady=2.5)

		email_pass = Label(frame, text="Email Password")
		email_pass.grid(row=2, column=0, padx=5, pady=2.5)

		email_receiver = Label(frame, text="To")
		email_receiver.grid(row=3, column=0, padx=5, pady=2.5)

		email_subject = Label(frame, text="Subject")
		email_subject.grid(row=4, column=0, padx=5, pady=2.5)

		# Entry
		username_entry = Entry(frame, width=50)
		username_entry.grid(row=1, column=1, padx=5, pady=2.5)

		pass_entry = Entry(frame, width=50, show='*')
		pass_entry.grid(row=2, column=1, padx=5, pady=2.5)

		self.receiver_entry = Entry(frame, width=50)
		self.receiver_entry.grid(row=3, column=1, padx=5, pady=2.5)

		subject_entry = Entry(frame, width=50)
		subject_entry.grid(row=4, column=1, padx=5, pady=2.5)

		body_entry = scrolledtext.ScrolledText(frame, height=14, width=58)
		body_entry.grid(row=5, column=0, padx=5, pady=10, columnspan=20)

		# Options Menu
		host_variable = StringVar(frame)
		host_variable.set("smtp.gmail.com:587") # default value

		w = OptionMenu(frame, host_variable, "smtp.gmail.com:587", "smtp.mail.yahoo.com:465", "smtp-mail.outlook.com:587")
		w.grid(row=0, column=1, padx=5, pady=2.5, columnspan=10)

		# Button
		send_button = Button(bottom_frame, text="Send", command=partial(self.send_email, host_variable, username_entry, pass_entry, 
																		subject_entry, self.email_generated, body_entry, window))
		send_button.pack(side=RIGHT)

		cancel_button = Button(bottom_frame, text="Cancel", command=window.destroy)
		cancel_button.pack(side=RIGHT)


	def send_email(self, _host, _username, _password, _subject, _toaddr, _body, window):
		host = _host.get()
		username = _username.get()
		password = _password.get()
		subject = _subject.get()
		tolist = _toaddr.get(1.0, END).split("\n")
		tolist.append(self.receiver_entry.get())
		body = _body.get(1.0, END)

		sender = EmailSender(host.split(":")[0], int(host.split(":")[1]))
		result = sender.send(username, password, tolist, subject, body)
		print(result)
		messagebox.showinfo("Info ", result)
		window.destroy()


	def initialize_message_extracting(self):
		frame_extracting = Frame(self.tab_email_extractor)
		frame_extracting.place(anchor='nw', relx=0.05, rely=0.05)

		# Label
		email_label = Label(frame_extracting, text="Email File: ")
		email_label.grid(row=0, column=0, padx=5.0, pady=2.5)

		dictionary_label = Label(frame_extracting, text="String Table: ")
		dictionary_label.grid(row=1, column=0, padx=5.0, pady=2.5)

		domain_label = Label(frame_extracting, text="Domain Mapping: ")
		domain_label.grid(row=2, column=0, padx=5.0, pady=2.5)

		result_label = Label(frame_extracting, text="Secret Message: ")
		result_label.grid(row=4, column=0, padx=5.0, pady=2.5)

		# Scrolled Text
		self.hidden_message = scrolledtext.ScrolledText(frame_extracting, width=90, height=19)
		self.hidden_message.grid(row=5, column=0, padx=5.0, pady=2.5, columnspan=20)

		# Entry
		self.email_entry = Entry(frame_extracting, width=50)
		self.email_entry.grid(row=0, column=1, padx=5.0, pady=2.5)

		self.ext_dictionary_entry = Entry(frame_extracting, width=50)
		self.ext_dictionary_entry.grid(row=1, column=1, padx=5.0, pady=2.5)

		self.ext_domain_entry = Entry(frame_extracting, width=50)
		self.ext_domain_entry.grid(row=2, column=1, padx=5.0, pady=2.5)

		# Button
		browse_email_button = Button(frame_extracting, text="Browse", command=partial(self.browse_plaintext, self.email_entry))
		browse_email_button.grid(row=0, column=2, padx=5.0, pady=2.5)

		browse_dictionary_button = Button(frame_extracting, text="Browse", command=partial(self.browse_plaintext, self.ext_dictionary_entry))
		browse_dictionary_button.grid(row=1, column=2, padx=5.0, pady=2.5)

		browse_domain_button = Button(frame_extracting, text="Browse", command=partial(self.browse_plaintext, self.ext_domain_entry))
		browse_domain_button.grid(row=2, column=2, padx=5.0, pady=2.5)

		extract_button = Button(frame_extracting, text="Extract", command=self.extract_message)
		extract_button.grid(row=3, column=0, padx=5.0, pady=10)

		save_hidden_message_button = Button(frame_extracting, text="Save", command=partial(self.save_to_file, self.hidden_message))
		save_hidden_message_button.grid(row=6, column=0, padx=5.0, pady=2.5)


	def extract_message(self):
		email_path = self.email_entry.get()
		dict_path = self.ext_dictionary_entry.get()
		domain_path = self.ext_domain_entry.get()

		try:
			if len(email_path) == 0 or len(domain_path) == 0 or len(dict_path) == 0:
				raise Exception("Please select the email file, dictionary and domain mapping !")
			if not isfile(email_path) or not isfile(domain_path) or not isfile(dict_path):
				raise Exception("Cannot find the specified file !")

			# Read the email file
			with open(email_path, 'r') as infile:
				content = infile.readlines()
			emails = [x.split("\n")[0].split(',')[0] for x in content]

			# Extract compressed message
			start = time.clock()
			extractor = MessageExtractor(domain_path)
			compressed = extractor.extract(emails)

			# Decompress the message
			decompressed = extractor.get_message(compressed, dict_path)
			end = time.clock()

			self.hidden_message.delete(1.0, END)
			self.hidden_message.insert(INSERT, decompressed)

			summary = "Elapsed Time = " + str(end-start) + " seconds\n"
			messagebox.showinfo("Summary", summary)

		except Exception as e:
			messagebox.showerror("Exception Found: ", str(e))


	def save_to_file(self, source):
		f = filedialog.asksaveasfile(initialdir="/", title="Select File", mode='wb')
		if f is None:
			return
		saveitem = source.get(1.0, END)
		saveitem = saveitem[:-1]
		item = [ord(x) for x in saveitem]
		f.write(bytes(item))
		f.close()


if __name__ =="__main__":
	root = Tk()
	root.geometry('800x600')
	root.title("LZWHeadStega")
	window = Window(root)
	root.mainloop()