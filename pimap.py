
import imaplib
import email
import getpass
import re

class Mail():

	def __init__(self, debug=False):
		self.server_configurations = {}
		self.email_credentials = {}
		self.mailboxes_names_to_check = {}


		# Will hold connection to server
		self.con = None
		self.connected_domain = ''
		self.connected_user = ''

		# debug
		self.debug = debug

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
		except:
			print("[ e ] Adding server configuration failed for:", domain, server_address, server_port)

	def show_server_config(self, domain="ALL"):
		"""
		Shows configuration for designated domain.
		Id domain parameter is omitted - shows all available configurations.
		:param domain: ex.: gmail.com
		:return:
		"""
		if domain == "ALL":
			for server_domain in self.server_configurations.keys():
				print(server_domain, '\t', self.server_configurations[server_domain][0] +':'+ str(self.server_configurations[server_domain][1]))
		else:
			if domain in self.server_configurations.keys():
				print(domain, '\t', self.server_configurations[domain][0] +':'+ str(self.server_configurations[domain][1]))
			else:
				print("[ e ] No configuration for domain:", domain)

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
				password = getpass.getpass('Password for '+ username + '@' + domain + ': ')

				if domain in self.email_credentials:
					self.email_credentials[domain].update({username : [password, mailbox_name]})
				else:
					self.email_credentials.update({domain : {username : [password, mailbox_name]}})
		except:
			print("[ e ] Adding credential configuration failed for:", domain, username)

	def show_account_credentials(self, domain='ALL'):
		"""
		Shows configured accounts for given domain.
		If domain parameter is omitted, shows all configuration.
		:param domain:
		:return:
		"""
		if domain == "ALL":
			for server_domain in self.email_credentials.keys():
				print(server_domain)

				for user in self.email_credentials[server_domain].keys():
					print('\t', user +':'+ self.email_credentials[server_domain][user][0], '\tBOX:', self.email_credentials[server_domain][user][1] )

		else:
			if domain in self.email_credentials.keys():
				print(domain)
				for user in self.email_credentials[domain].keys():
					print('\t', user +':'+ self.email_credentials[domain][user][0], '\tBOX:', self.email_credentials[domain][user][1] )
			else:
				print("[ e ] No configuration for domain:", domain)

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
				print("[ e ] Unable to establish IMAP4_SSL connection.", )
		else:
			print("[ e ] Unable to establish connection. No configuration for domain:", domain)

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
						print('[ e ] Login unsuccessful.', error)
			else:
				print("[ e ] Unable to login. Connected to domain:", self.connected_domain, ". Login attempt to domain:", domain)

		if result is not None and len(result) > 0:
			if result[0] == "OK":
				print('Logon successful.')
				self.connected_user = user
				return 0

		return -1

	def logoff(self):
		"""
		Logs off from current mailbox connection.
		:return:
		"""
		self.con.logout()

	def close(self):
		"""
		Closes currently opened mailbox.
		:return:
		"""
		self.con.close()

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
			check, stats = self.con.status(self.email_credentials[domain][user][1], '(MESSAGES UNSEEN)')

			if check == 'OK':
				# Cleanse info
				stats_data = list((stats[0]).decode('latin-1').replace(self.email_credentials[domain][user][1],'').strip('"').strip().strip(')').split(' '))

				# Print notification
				print( adjust_string(user +'@'+ domain, 30),
				       self.email_credentials[domain][user][1],
				       stats_data[3] +'/'+ stats_data[1])
			else:
				# Notify about failure
				print('[ e ] Mailbox',
				      self.email_credentials[self.connected_domain][self.connected_user][1],
				      'is not available.' )

		except:
			print('[ e ] Mailbox check failed.')

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

		email_message = email.message_from_string(raw_email)
		print('\tTo:', email_message['To'])
		print('\tFr:', email_message['From'])
		print('\tSb:', email_message['Subject'])

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
			raw_email = raw_email.decode('utf-8')
			self.set_msg_as_unseen(uid)
		else:
			print('Fetching mail failed.',result)
		return raw_email




def main():

	mail = Mail(True)

	# Adds configuration
	mail.add_server_config('gmail.com', 'imap.gmail.com')
	mail.add_server_config('outlook.com', 'imap-mail.outlook.com')

	# Adding credentials
	mail.add_account_credentials('gmail.com', '')
	# mail.add_account_credentials('gmail.com', '')
	# mail.add_account_credentials('gmail.com', '')
	# mail.add_account_credentials('gmail.com', '')
	mail.add_account_credentials('outlook.com', '')
	# mail.add_account_credentials('outlook.com', '')
	# mail.add_account_credentials('outlook.com', '')

	# Showing configurations
	if mail.debug:
		mail.show_server_config()
		mail.show_account_credentials()

	# Login to mailbox
	mail.login('gmail.com', '')
	mail.check_mailbox_stats()
	#mail.check_message_unseen()

	unseen = mail.get_uids('UNSEEN')

	if len(unseen) > 0:
		unseen_all = unseen[0].split()
		print(unseen_all)
		for uid in unseen_all:
			msg = mail.get_message_by_uid(uid)
			msg_parsed = mail.parse_message(msg)



	# mail.login('gmail.com', '')
	# mail.check_mailbox_stats()
	#
	# mail.login('gmail.com', '')
	# mail.check_mailbox_stats()
	#
	# mail.login('gmail.com', '')
	# mail.check_mailbox_stats()
	#
	mail.login('outlook.com', '')
	mail.check_mailbox_stats()

	unseen = mail.get_uids()

	if len(unseen) > 0:
		unseen_all = unseen[0].split()
		print(unseen_all)
		for uid in unseen_all:
			msg = mail.get_message_by_uid(uid)
			msg_parsed = mail.parse_message(msg)

	# mail.login('outlook.com', '')
	# mail.check_mailbox_stats()
	#
	# mail.login('outlook.com', '')
	# mail.check_mailbox_stats()




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