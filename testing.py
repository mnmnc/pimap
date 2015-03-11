import imaplib
import re

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
		print("[ i ] Fetching message", uid.decode('utf-8'))
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





def adjust_string(string, length):
	if length - len(string) > 0:
		for i in range(length - len(string)):
			string += ' '
		return string[:length]
	else:
		return string[:length]



def parse_list_response(line):
	list_response_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')

	flags, delimiter, mailbox_name = list_response_pattern.match(line.decode('iso-8859-1')).groups()
	mailbox_name = mailbox_name.strip('"')
	return (flags, delimiter, mailbox_name)

def main():

	g = Gmail('@gmail.com', '', 'imap.gmail.com')
	g.login()
	g.goto_inbox()
	g.get_uid()

	print(g.connection.check())
	print(g.connection.namespace())

	# LISTING DIRECTORIES
	#print(g.connection.lsub('/INBOX','*'))

	# LISTING MAILBOXES
	result, mailboxes = g.connection.list()
	for mailbox in mailboxes:
		print(mailbox)

		flags, delimiter, mailbox_name = parse_list_response(mailbox)
		print(flags, delimiter, mailbox_name)

		# GET MAILBOX PROPERTIES / UNSEEN MAILS
		print(g.connection.status(mailbox_name, '(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)'))

		# GET NUMEBER OF MESSAGES IN MAILBOX
		try:
			typ, data = g.connection.select(mailbox_name)
			print(typ, data)
			num_msgs = int(data[0])
			print('There are %d messages in folder' % num_msgs)
		except:
			pass

	#print(g.connection.list(pattern=('*Wys*')))

		# GETTING PARTIAL INFO FROM MESSAGE NUMBER 1
		try:
			g.connection.select(mailbox_name, readonly=True)
			typ, msg_data = g.connection.fetch('1', '(BODY.PEEK[HEADER] FLAGS)')
			print(msg_data)
		except:
			pass

		# GETTING PARTIAL INFO FROM MESSAGE NUMBER 1 SEPARATELY
		try:
			g.connection.select('INBOX', readonly=True)

			print('HEADER:')
			typ, msg_data = g.connection.fetch('1', '(BODY.PEEK[HEADER])')
			for response_part in msg_data:
				if isinstance(response_part, tuple):
					print(response_part[1])

			print('BODY TEXT:')
			typ, msg_data = g.connection.fetch('1', '(BODY.PEEK[TEXT])')
			for response_part in msg_data:
				if isinstance(response_part, tuple):
					print(response_part[1])

			print('\nFLAGS:')
			typ, msg_data = g.connection.fetch('1', '(FLAGS)')
			for response_part in msg_data:
				print(response_part)
				print(imaplib.ParseFlags(response_part))
		except: pass

		try:
			import email
			g.connection.select('INBOX', readonly=True)

			typ, msg_data = g.connection.fetch('1', '(RFC822)')
			for response_part in msg_data:
				if isinstance(response_part, tuple):
					msg = email.message_from_string(response_part[1].decode('latin-1'))
					for header in [ 'subject', 'to', 'from' ]:
						print('%-8s: %s' % (header.upper(), msg[header]))
		except: print('--------------------------Failure')
	g.close()




if __name__ == "__main__":
	main()
