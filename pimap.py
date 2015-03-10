
import imaplib
import email

class Gmail():

	def __init__(self, email, password, server):
		self.email = email
		self.password = password
		self.server = server
		self.uid = []
		self.connection = imaplib.IMAP4_SSL(self.server)

	def login(self):
		result = self.connection.login(self.email, self.password)
		if result[0] == "OK":
			print("[NFO] AUTH SUCCESSFUL.")

	def goto_inbox(self):
		self.connection.select("inbox")

	def get_uid(self):
		result, data = self.connection.uid('search', None, "ALL")
		if result == "OK":
			self.uid = (data[0]).split()
			print("[NFO] UIDs fetched.")
		else:
			print("[ERR] Searching for UIDs failed.")

	def fetch_by_uid(self, uid):
		raw_email = ''
		print("[NFO] Fetching message", uid.decode('utf-8'))
		result, data = self.connection.uid('fetch', uid, '(RFC822)')
		if result == "OK":
			raw_email = data[0][1]
		return raw_email


	def close(self):
		self.connection.close()

	def parse_email(self, raw_email):
		email_message_for_headers = email.message_from_string(str(raw_email.decode('utf-8')))
		email_head = email_message_for_headers.items()
		email_char_arr = ['iso-8859-2', 'latin-1', 'utf-8', 'iso-8859-1']
		email_char = ''
		email_message = 'Unable to decode'
		try:
			for h in email_head:
				print(h)
				if h[0].upper() == 'Content-type'.upper():
					print("\tCharset:", (h[1].split("charset=")[1]))
					email_char = h[1].split("charset=")[1]
		except:
			print('[ERR] Encoding missing')

		if email_char == '':
			for char in email_char_arr:
				try:
					email_message = email.message_from_string(str(raw_email.decode(char)))
					break
				except:
					pass
		else:
			try:
				email_message = email.message_from_string(str(raw_email.decode(email_char)))
			except:
				pass

		email_to = email_message_for_headers['To']
		email_from = email.utils.parseaddr(email_message_for_headers['From'])

		email_type = email_message_for_headers.get_content_maintype()



		print()
		print("To:", email_to)
		print("From:", email_from)
		print("Head:")


		email_text = self.get_text(email_message)

		print("Maintype:", email_type)
		print("Text:", email_text)


	def get_text(self, email_message_instance):
		maintype = email_message_instance.get_content_maintype()
		if maintype == 'multipart':
			for part in email_message_instance.get_payload():
				if part.get_content_maintype() == 'text':
					return part.get_payload()
		elif maintype == 'text':
			return email_message_instance.get_payload()

def main():

	g = Gmail('a@gmail.com', '', 'imap.gmail.com')
	g.login()
	g.goto_inbox()
	g.get_uid()
	#raw_email = g.fetch_by_uid(b'10544')
	#g.parse_email(raw_email)
	for uid in g.uid:
		raw_email = g.fetch_by_uid(uid)
		g.parse_email(raw_email)

	g.close()

if __name__ == "__main__":
	main()

def test():
	mail = imaplib.IMAP4_SSL('imap.gmail.com')
	mail.login('a@gmail.com', '')
	mail.list()
	# Out: list of "folders" aka labels in gmail.
	mail.select("inbox") # connect to inbox.

	result, data = mail.uid('search', None, "ALL") # search and return uids instead

	ids = data[0] # data is a list.
	id_list = ids.split() # ids is a space separated string

	print(result)
	latest_email_uid = data[0].split()[-1]

	result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')

	raw_email = data[0][1] # here's the body, which is raw text of the whole email
	# including headers and alternate payloads

	print(latest_email_uid)
	s = str(raw_email.decode('utf-8'))



	mail.close()


	import email
	email_message = email.message_from_string(s)

	print(email_message['To'])

	print(email.utils.parseaddr(email_message['From'])) # for parsing "Yuji Tomita" <yuji@grovemade.com>

	print(email_message.items()) # print all headers

	# note that if you want to get text content (body) and the email contains
	# multiple payloads (plaintext/ html), you must parse each message separately.
	# use something like the following: (taken from a stackoverflow post)
	def get_first_text_block(self, email_message_instance):
		maintype = email_message_instance.get_content_maintype()
		if maintype == 'multipart':
			for part in email_message_instance.get_payload():
				if part.get_content_maintype() == 'text':
					return part.get_payload()
		elif maintype == 'text':
			return email_message_instance.get_payload()

