
import imaplib
import email
import getpass
import re
import sys
import quopri
import base64
import time
import datetime



class Mail():

	def __init__(self, debug=False):

		self.server_configurations = {}
		self.email_credentials = {}
		self.mailboxes_names_to_check = {}
		self.emails = []


		# Will hold connection to server
		self.con = None
		self.connected_domain = ''
		self.connected_user = ''

		# variables
		self.show_messages = False

		# debug
		self.debug = debug
		self.log = ''

	def print_notification(self, type, length, title, details):
		notification_types = ['ERROR', 'INFO', 'WARNING', 'SUCCESS', 'CHOICE', 'SUB', 'INPUT']
		title_length = length
		details_length = 50
		if type.upper() in notification_types:
			if type.upper() == 'ERROR':
				print('[ ERR ]',
				      adjust_string(title, title_length),
				      adjust_string(details, details_length)
				)
			elif type.upper() == 'INFO':
				print('[ NFO ]',
				      adjust_string(title, title_length),
				      adjust_string(details, details_length)
				)
			elif type.upper() == 'WARNING':
				print('[ WRG ]',
				      adjust_string(title, title_length),
				      adjust_string(details, details_length)
				)
			elif type.upper() == 'SUCCESS':
				print('[ SUC ]',
				      adjust_string(title, title_length),
				      adjust_string(details, details_length)
				)
			elif type.upper() == 'CHOICE':
				print('[ CHC ]',
				      adjust_string(title, title_length),
				      adjust_string(details, details_length)
				)
			elif type.upper() == 'SUB':
				print('       ',
				      adjust_string(title, title_length),
				      adjust_string(details, details_length)
				)
			elif type.upper() == 'INPUT':
				print('[ INP ]',
				      adjust_string(title, title_length),
				      adjust_string(details, 0),
				      end=': '
				)

	def add_server_config(self, domain, server_address, server_port=993):
		"""
		Adds server configuration for designated domain
		:param domain: ex.: gmail.com
		:param server_address: ex.: imap.gmail.com
		:param server_port: ex.: 993 (default)
		:return:
		"""
		try:
			self.server_configurations.update({domain: [server_address, server_port] })
			if self.debug:
				self.print_notification('success', 35,'Server configuration added:', domain)
		except:
			if self.debug:
				self.print_notification('error', 35, 'Failed to add configuration for', domain)

	def show_server_config(self, domain="ALL"):
		"""
		Shows configuration for designated domain.
		Id domain parameter is omitted - shows all available configurations.
		:param domain: ex.: gmail.com
		:return:
		"""

		if domain == "ALL":
			self.print_notification('info', 35, 'Available configurations:','')
			for server_domain in self.server_configurations.keys():
				self.print_notification('sub', 35, server_domain,
				                        self.server_configurations[server_domain][0]
				                        +':'+
				                        str(self.server_configurations[server_domain][1])
				)
			print()
		else:
			if domain in self.server_configurations.keys():
				self.print_notification('info', 35, 'Configuration for ' + domain + ':',
				                        self.server_configurations[domain][0]
				                        +':'+
				                        str(self.server_configurations[domain][1]))

			else:
				self.print_notification('error', 35, 'Configuration unavailable for:', domain)

	def add_account_credentials(self, domain, username, password='PromptMe', mailbox_name='Inbox'):
		"""
		Adds credentials for designated domain/username.
		:param domain:
		:param username:
		:param password:
		:return:
		"""
		try:
			if password == 'PromptMe':
				self.print_notification('input', 35, 'Password for '+ username + '@' + domain, '')
				sys.stdout.flush()
				password = getpass.getpass('')

				if domain in self.email_credentials:
					self.email_credentials[domain].update({username : [password, mailbox_name]})
				else:
					self.email_credentials.update({domain : {username : [password, mailbox_name]}})
		except:
			self.print_notification('error', 35, 'Failed to add credentails for:', username + '@' + domain)

	def show_account_credentials(self, domain='ALL'):
		"""
		Shows configured accounts for given domain.
		If domain parameter is omitted, shows all configuration.
		:param domain:
		:return:
		"""
		if domain == "ALL":
			self.print_notification('info', 35, 'Configured credentials:', '')
			for server_domain in self.email_credentials.keys():
				for user in self.email_credentials[server_domain].keys():
					self.print_notification('sub', 35,
					                        user + '@' + server_domain + ' / ' +
					                        self.email_credentials[server_domain][user][1],
					                        self.email_credentials[server_domain][user][0]
					                        )
			print()

		else:
			if domain in self.email_credentials.keys():
				self.print_notification('info', 35, 'Configured credentials:', '')
				for user in self.email_credentials[domain].keys():
					self.print_notification('sub', 35,
					                        user + '@' + domain + ' / ' +
					                        self.email_credentials[domain][user][1],
					                        self.email_credentials[domain][user][0]
					                        )
				print()
			else:
				self.print_notification('error', 35, 'No configuration available for:', domain)

	def connect(self, domain):
		"""
		Connects to designated domain using adequate configuration.
		:param domain: ex.: gmail.com
		:return:
		"""
		try:
			self.logoff()   # If the previous connection exists
		except:
			pass

		if domain in self.server_configurations.keys():
			try:
				self.con = imaplib.IMAP4_SSL(self.server_configurations[domain][0], self.server_configurations[domain][1])
				self.connected_domain = domain
			except:
				if self.debug:
					self.print_notification('error', 35, 'IMAP4_SSL connection failure:', domain)

		else:
			self.log += 'Error. No configuration for domain:' + domain + '\n'
			if self.debug:
				self.print_notification('error', 35, 'No configuration for domain:', domain)

	def login(self, domain, user):
		"""
		Logs in to the IMAP server of designated domain.
		:param domain: ex.: gmail.com
		:param user: ex.: user1
		:return:
		"""
		# CONNECT TO IMAP SERVER
		self.connect(domain)

		result = None
		if domain == self.connected_domain:
			if domain in self.email_credentials.keys():
				if user in self.email_credentials[domain].keys():
					try:
						result = self.con.login(user + '@' + domain, self.email_credentials[domain][user][0])
					except Exception as err:
						error = str(err.args[0].decode('utf-8'))
						self.print_notification('error', 35, 'Login unsuccessful:', error)
				else:
					self.print_notification('error', 35, 'No credentials for:', user + '@' + domain)
			else:
				self.print_notification('error', 35, 'No credentials for:', domain)
		else:
			self.print_notification('error', 35, 'Domain mismatch:', domain + '!=' + self.connected_domain)

		if result is not None and len(result) > 0:
			if result[0] == "OK":
				if self.debug:
					self.print_notification('success', 35, 'Logon successful:', user + '@' + domain)
				self.connected_user = user
				return 0
		return -1

	def logoff(self):
		"""
		Logs off from current mailbox connection.
		:return:
		"""
		logoff_result = self.con.logout()[0]
		if self.debug:
			self.print_notification('info', 35, 'Logoff:', logoff_result )

	def close(self):
		"""
		Closes currently opened mailbox.
		:return:
		"""
		self.print_notification('info', 35, 'Closing connection:', self.con.close()[0])

	def check_mailbox_stats(self):
		"""
		Checks how many messages are in the mailbox.
		Checks number of unread messages.
		"""

		# Local vars
		domain = self.connected_domain
		user = self.connected_user


		try:
			# Get info
			mailbox = self.email_credentials[domain][user][1]
			check, stats = self.con.status(self.email_credentials[domain][user][1], '(MESSAGES UNSEEN)')

			if check == 'OK':
				# Cleanse info
				stats_data = list((stats[0]).decode('latin-1').replace(mailbox,'').strip('"').strip().strip(')').split(' '))
				all_messages = stats_data[1]
				unseen_messages = stats_data[3]

				# Print notification
				self.print_notification('info', 35, user +'@'+ domain + ' / ' + mailbox, unseen_messages +'/'+ all_messages)

			else:
				# Notify about failure
				self.print_notification('error', 35, 'Mailbox unavailable:', user +'@'+ domain + ' / ' + mailbox)

		except Exception as err:
			self.print_notification('error', 35, 'Mailbox status check failed:',err.args[0])


	def check_message_details(self, id):

		# TODO:
		# TODO: is this used?
		# TODO:

		self.con.select(self.email_credentials[self.connected_domain][self.connected_user][1], readonly=False)
		check, msg_data = self.con.fetch(id.decode('utf-8'), '(BODY.PEEK[HEADER] FLAGS)')

		self.parse_message(msg_data[1])

	def check_message_unseen(self):

		# TODO:
		# TODO: is this used?
		# TODO:

		self.con.select(self.email_credentials[self.connected_domain][self.connected_user][1], readonly=False)
		check, msg_data = self.con.search(None, 'UNSEEN')

		for msg_id in msg_data[0].split():
			self.check_message_details(msg_id)

	def parse_message(self, raw_email):
		"""
		Gets information from message headers.
		"""

		# TODO: extend capabilities
		self.print_notification('info', 35, 'Checking message inner details:','')
		self.check_message_inner_details(raw_email)

		#email_message = email.message_from_string(raw_email.decode('latin-1'))


		#self.print_message(email_message, ['To', 'From', 'Received', 'Subject', 'Date'])
		# print(email_message.keys())
		# print('\tTo:', email_message['To'])
		# print('\tFr:', email_message['From'])
		# print('\tSb:', email_message['Subject'])

	def parse_header(self, header):
		print('quopri:',quopri.decodestring(header))
		(text, encoding) = email.header.decode_header(header)[0]
		return text


	def check_message_inner_details(self, raw_email):

		email_message_latin = ''
		email_message_utf8 = ''
		email_message_iso88591 = ''
		email_message_iso88592 = ''
		print('Begin')

		try:
			email_message_latin = email.message_from_string(raw_email.decode('latin-1'))

			print(email_message_latin['To'])

		except:
			print('E latin')
			pass

		try:
			email_message_utf8 = email.message_from_string(raw_email.decode('utf-8'))
			self.parse_header(email_message_utf8['Subject'])
			print(email_message_utf8['Subject'])
		except:
			print('E utf')
			pass

		try:
			email_message_iso88591 = email.message_from_string(raw_email.decode('iso-8859-1'))
			print(email_message_iso88591['To'])
		except:
			print('E 88591')
			pass

		try:
			email_message_iso88592 = email.message_from_string(raw_email.decode('iso-8859-2'))
			print(email_message_iso88592['To'])
		except:
			print('E 88592')
			pass

		if email_message_latin == '':
			print('latin failed')

		if email_message_utf8 == '':
			print('utf8 failed')
		if email_message_iso88591 == '':
			print('iso88591 failed')
		if email_message_iso88592 == '':
			print('iso88592 failed')

		print('End')


	def print_message(self, email_message, fields, verbosity='0'):
		print(email_message)

		if verbosity == '0':
			for field in fields:
				if field in email_message.keys():
					values = email_message.get_all(field)
					for value in values:
						self.print_notification('sub', 35, field, value)

		elif verbosity == '1':
			pass
		elif verbosity.upper() == 'multiline':
			pass
		else:
			pass


	def set_msg_as_seen(self, id):
		"""
		Sets SEEN attribute for message with given ID.
		"""
		self.con.uid('STORE', id , '+FLAGS', '(\\SEEN)')

	def set_msg_as_unseen(self, id):
		"""
		Removes SEEN attribute from message with given ID.
		"""
		self.con.uid('STORE', id , '-FLAGS', '(\\SEEN)')

	def get_uids(self, scope="ALL"):
		"""
		Gets unique identifiers of messages from given scope.
		:param scope: ALL UNSEEN SEEN
		"""
		self.con.select(self.email_credentials[self.connected_domain][self.connected_user][1], readonly=False)
		result, data = self.con.uid('search', None, scope)
		if result == 'OK':
			if len(data) > 0:
				return data[0].split()
		return []

	def get_message_by_uid(self, uid):
		"""
		Fetches email message with given uid.
		:param uid: '1'
		:return: raw email string
		"""
		raw_email = ''
		result, data = self.con.uid('fetch', uid, '(RFC822)')
		if result == 'OK':
			#print(data)
			raw_email = data[0][1]
			self.set_msg_as_unseen(uid)
			self.print_notification('success', 35, 'Email fetched:', str(uid))
		else:
			self.print_notification('error', 35, 'Fetching email failed for:', str(uid))
		return raw_email

	def get_message_peek_by_uid(self, uid):

		raw_email = ''
		result, data = self.con.uid('fetch', uid, '(BODY.PEEK[HEADER])')
		if result == 'OK':

			email_message = email.message_from_string(data[0][1].decode('latin-1'))
			return (uid, email_message)
		return (None, None)

	def print_default_headers(self, email_message, uid, inline=False):
		if inline:
			print('\t' + adjust_string(str(uid.decode('utf-8')), 10), end='\t')
			print(adjust_string(email.utils.parseaddr(email_message["To"])[1], 30), end='\t')
			print(adjust_string(email.utils.parseaddr(email_message["From"])[1],30), end='\t')
			print(adjust_string(email_message["Subject"], 30), end='\t')
			print()
		else:
			print()
			print('\tID:  ', adjust_string(str(uid.decode('utf-8')), 10))
			print('\tTo:  ', email.utils.parseaddr(email_message["To"])[1])
			print('\tFrom:', email.utils.parseaddr(email_message["From"])[1])
			print('\tSubject: ', email_message["Subject"])



def main():

	mail = Mail(False)

	# Adds configuration
	mail.add_server_config('gmail.com', 'imap.gmail.com')
	mail.add_server_config('outlook.com', 'imap-mail.outlook.com')

	# Adding credentials
	mail.add_account_credentials('gmail.com', '')
	mail.add_account_credentials('gmail.com', '')
	mail.add_account_credentials('gmail.com', '')
	mail.add_account_credentials('gmail.com', '')
	mail.add_account_credentials('outlook.com', '')
	mail.add_account_credentials('outlook.com', '')
	mail.add_account_credentials('outlook.com', '')

	# Showing configurations
	if mail.debug:
		mail.show_server_config()
		mail.show_server_config('test.com')
		mail.show_server_config('outlook.com')
		mail.show_account_credentials()
		mail.show_account_credentials('outlook.com')
		mail.show_account_credentials('sdsad.com')

	# Login to mailboxes
	while True:

		print('----------- ' + str(datetime.datetime.now()) + ' -----------')

		for domain in mail.email_credentials:
			if domain in mail.server_configurations:
				for user in mail.email_credentials[domain]:

					if mail.debug:
						mail.print_notification('info', 35, 'Current user:', user + '@' + domain)
					check = mail.login(domain, user)
					if check == 0:
						mail.check_mailbox_stats()

						unseen = mail.get_uids('UNSEEN')

						if len(unseen) > 0:
							for uid in unseen:
								#msg = mail.get_message_by_uid(uid)
								id, msg = mail.get_message_peek_by_uid(uid)
								if msg is not None and mail.show_messages:
									mail.print_default_headers(msg, id, True)
		time.sleep(20)


	# CLEAN UP
	mail.logoff()

def adjust_string(string, length):
	"""
	Adjusts string to specified length.
	:param string:
	:param length:
	:return:
	"""
	if length - len(string) > 0:
		for i in range(length - len(string)):
			string += ' '
		return string[:length]
	else:
		return string[:length]

if __name__ == "__main__":
	main()