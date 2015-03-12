

import imaplib
import email

class Gmail():

	def __init__(self, email, password, server):
		"""
		Initializes the mail connection object.
		:param email: your email address
		:param password: your password
		:param server: server address
		:return:
		"""
		self.email = email
		self.password = password
		self.server = server
		self.uid = []
		self.connection = imaplib.IMAP4_SSL(self.server)
		self.unique_head = []

	def login(self):
		"""
		Logs in to the email server and establishes connection.
		:return:
		"""
		result = self.connection.login(self.email, self.password)
		if result[0] == "OK":
			print("[ i ] LOGIN SUCCESSFUL.")

	def goto_inbox(self):
		"""
		Sets the context to inbox folder.
		:return:
		"""
		self.connection.select("inbox")

	def get_uid(self):
		"""
		Searches for all UIDs in the designated folder.
		:return:
		"""
		result, data = self.connection.uid('search', None, "ALL")
		if result == "OK":
			self.uid = (data[0]).split()
			print("[ i ] UIDs fetched.")
		else:
			print("[ e ] Searching for UIDs failed.")

	def fetch_by_uid(self, uid):
		"""
		Gets an email by UID.
		:param uid: designated UID
		:return:
		"""
		raw_email = ''
		#print("[ i ] Fetching message", uid.decode('utf-8'))
		result, data = self.connection.uid('fetch', uid, '(RFC822)')
		if result == "OK":
			raw_email = data[0][1]
		return raw_email


	def close(self):
		"""
		Closes connection.
		:return:
		"""
		self.connection.close()

	def parse_email(self, raw_email):
		"""
		Parses email to get details.
		:param raw_email: raw email content.
		:return:
		"""

		# SEARCHING FOR CORRECT CHARSET
		email_message_for_headers = email.message_from_string(str(raw_email.decode('latin-1')))
		email_head = email_message_for_headers.items()
		email_char_arr = ['iso-8859-2', 'latin-1', 'utf-8', 'iso-8859-1']
		email_char = ''


		email_message = 'Unable to decode'

		# TRYING TO GET CHARSET FROM EMAIL
		try:
			for header in email_head:
				if header[0].upper() == 'CONTENT-TYPE':
					email_char = header[1].split("charset=")[1]
		except:
			print('[ e ] Encoding missing')

		# IF ENCODING IS MISSING
		if email_char == '':
			# TRY KNOWN ENCODINGS
			for char in email_char_arr:
				try:
					email_message = email.message_from_string(str(raw_email.decode(char)))
					# BREAK IN CASE OF SUCCESS
					break
				except:
					pass

		# IF ENCODING IS KNOWN
		else:
			try:
				email_message = email.message_from_string(str(raw_email.decode(email_char)))
			except:
				print('[ e ] Failed to decode message with', email_char)
				pass


		# GETTING BASIC INFO FROM HEADERS
		email_to = email_message_for_headers['To']
		email_from = email.utils.parseaddr(email_message_for_headers['From'])
		email_type = email_message_for_headers.get_content_maintype()

		# for h in email_head:
		# 	print(h)
		d = email_message_for_headers['Date']

		email_delivered_to = email_message_for_headers['Delivered-To']
		email_received = email_message_for_headers['Received']
		email_reply_to = email_message_for_headers['Reply-To']
		email_message_id = email_message_for_headers['Message-ID']

		# GET TEXT FROM MESSAGE
		email_text = self.get_text(email_message)


		print()
		print("To:", email_to)
		print("From:", email_from)
		print("Date:", d)
		print("Received:", email_received)

		print("Maintype:", email_type)
		#print("Text:", email_text)
		print("Message:", email_message)

	def get_text(self, email_message_instance):
		maintype = email_message_instance.get_content_maintype()
		if maintype == 'multipart':
			for part in email_message_instance.get_payload():
				if part.get_content_maintype() == 'text':
					return part.get_payload()
		elif maintype == 'text':
			return email_message_instance.get_payload()

	def get_headers(self, raw_email):
		"""
		Parses email to get headers.
		:param raw_email: raw email content.
		:return:
		"""
		email_message = email.message_from_string(str(raw_email.decode('latin-1')))
		email_head = email_message.items()

		# for h in email_head:
		# 	print("\t",h[0], h[1])

		email_dictionary = {}

		delivered_to = []
		received = []
		xreceived = []
		return_path = []
		received_spf = []
		mime = []
		date = []
		message_id = []
		subject = []
		email_from = []
		email_to = []
		content_type = []
		xforwarded_to = []
		xforwarded_for = []
		xmailer = []
		xvirus_scanned = []


		for header in email_head:

			if header[0].upper() == "Delivered-To".upper():
				delivered_to.append(header[1])
			elif header[0].upper() == "Received".upper():
				received.append(header[1])
			elif header[0].upper() == "X-Received".upper():
				xreceived.append(header[1])
			elif header[0].upper() == "Return-Path".upper():
				return_path.append(header[1])
			elif header[0].upper() == "Received-SPF".upper():
				received_spf.append(header[1])
			elif header[0].upper() == "MIME-Version".upper():
				mime.append(header[1])
			elif header[0].upper() == "Date".upper():
				date.append(header[1])
			elif header[0].upper() == "Message-ID".upper():
				message_id.append(header[1])
			elif header[0].upper() == "Subject".upper():
				subject.append(header[1])
			elif header[0].upper() == "From".upper():
				email_from.append(email.utils.parseaddr(header[1]))
			elif header[0].upper() == "To".upper():
				email_to.append(email.utils.parseaddr(header[1]))
			elif header[0].upper() == "Content-Type".upper():
				content_type.append(header[1])
			elif header[0].upper() == "X-Forwarded-To".upper():
				xforwarded_to.append(header[1])
			elif header[0].upper() == "X-Forwarded-For".upper():
				xforwarded_for.append(header[1])
			elif header[0].upper() == "X-Mailer".upper():
				xmailer.append(header[1])
			elif header[0].upper() == "X-Virus-Scanned".upper():
				xvirus_scanned.append(header[1])

		email_content = {
			'delivered_to': delivered_to,
			'received': received,
			'xreceived': xreceived ,
			'return_path': return_path,
			'received_spf': received_spf,
			'mime': mime,
			'date': date,
			'message_id': message_id,
			'subject': subject,
			'from': email_from,
			'to': email_to,
			'content_type': content_type,
			'xforwarded_to': xforwarded_to,
			'xforwarded_for': xforwarded_for,
			'xmailer': xmailer,
			'xvirus_scanned': xvirus_scanned
		}

		return email_content

# Delivered-To
# Received
# X-Received
# Return-Path
# Received
# Received-SPF
# Authentication-Results
# Received
# Return-Path
# Received-SPF
# X-Received
# DKIM-Signature
# MIME-Version
# X-Received
# Received
# Received
# Date
# Message-ID
# Subject
# From
# To
# Content-Type
# Content-Transfer-Encoding
# X-Forwarded-To
# X-Forwarded-For
# X-Mailer
# X-Virus-Scanned


		#
		# email_delivered_to = email_message['Delivered-To']
		# email_received = email_message['Received']
		# email_x_received = email_message['X-Received']
		# email_return_path = email.utils.parseaddr(email_message['Return-Path'])[0]
		#
		# email_to = email_message['To']
		# email_from = email.utils.parseaddr(email_message['From'])
		# email_type = email_message.get_content_maintype()
		# email_date = email_message['Date']
		#
		# print(email_delivered_to)
		# print(email_received)
		# print(email_x_received)
		# print(email_return_path)
		#
		# print(email_message['Received'])
		#
		# print(email_head[0])


	def print_head(self):
		for hh in self.unique_head:
			print(hh)

def adjust_string(string, length):
	if length - len(string) > 0:
		for i in range(length - len(string)):
			string += ' '
		return string[:length]
	else:
		return string[:length]

def main():

	g = Gmail('@gmail.com', '', 'imap.gmail.com')
	g.login()
	g.goto_inbox()
	g.get_uid()

	for uid in g.uid:
		raw_email = g.fetch_by_uid(uid)
		#g.parse_email(raw_email)
		email_headers = g.get_headers(raw_email)
		print("\n", adjust_string(str(uid.decode('utf-8')), 8), end="\t")

		# TO
		if len(email_headers['to']) > 0 and email_headers['to'][0][1]:
			print(adjust_string(email_headers['to'][0][1], 30), end=' ')
		else:
			print(adjust_string('-',30), end=' ')

		# FROM
		if len(email_headers['from']) > 0 and email_headers['from'][0][1]:
			print(adjust_string(email_headers['from'][0][1], 30), end=' ')
		else:
			print(adjust_string('-',30), end=' ')

		# SUBJECT
		if len(email_headers['subject']) > 0:
			print(adjust_string(email_headers['subject'][0], 30), end=' ')
		else:
			print(adjust_string('-',30), end=' ')

		# XMAILER
		if len(email_headers['xmailer']) > 0:
			print(adjust_string(email_headers['xmailer'][0], 30), end=' ')
		else:
			print(adjust_string('-',30), end=' ')

		# for header in email_headers.keys():
		#
		# 	if len(email_headers[header]) > 1:
		# 		print(header)
		# 		for ele in email_headers[header]:
		# 			print("\t", ele)
		# 	else:
		# 		print(header, ': ', email_headers[header])


	g.print_head()
	g.close()




if __name__ == "__main__":
	main()






def test():
	"""

	:return:
	:rtype:
	"""
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

