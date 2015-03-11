
import imaplib
import email
import getpass

class Mail():

	def __init__(self):
		self.server_configurations = {}
		self.email_credentials = {}

		# Will hold connection to server
		self.con = None
		self.connected_domain = ''

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

	def add_account_credentials(self, domain, username, password='PromptMe'):
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
					self.email_credentials[domain].append([username, password])
				else:
					self.email_credentials.update({domain: [[username, password]]})
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

				for details in self.email_credentials[server_domain]:
					print('\t', details[0] +':'+ details[1])

		else:
			if domain in self.email_credentials.keys():
				print(domain)
				for details in self.email_credentials[domain]:
					print('\t', details[0] +':'+ details[1])
			else:
				print("[ e ] No configuration for domain:", domain)

	def connect(self, domain):
		"""
		Connects to designated domain using adequate configuration.
		:param domain: ex.: gmail.com
		:return:
		"""
		try:
			self.logoff()
		except:
			pass

		if domain in self.server_configurations.keys():
			self.con = imaplib.IMAP4_SSL(self.server_configurations[domain][0], self.server_configurations[domain][1])
			self.connected_domain = domain
		else:
			print("[ e ] Unable to establish connection. No configuration for domain:", domain)

	def login(self, domain, user):

		# CONNECT TO IMAP SERVER
		self.connect(domain)

		result = None
		if domain == self.connected_domain:
			if domain in self.email_credentials:
				for details in self.email_credentials[domain]:
					if details[0] == user:
						result = self.con.login(user + '@' + domain, details[1])
						break
		else:
			print("[ e ] Unable to login. Connected to domain:", self.connected_domain, ". Login attempt to domain:", domain)

		if result is not None and len(result) > 0:
			if result[0] == "OK":
				print('Logon successful.')
				return 0
		return -1

	def logoff(self):
		"""
		Logs off from current mailbox connection.
		:return:
		"""
		self.con.logout()

	def close(self):
		self.con.close()

def main():

	mail = Mail()
	mail.add_server_config('gmail.com', 'imap.gmail.com')
	mail.add_server_config('outlook.com', 'imap-mail.outlook.com')

	mail.add_account_credentials('gmail.com', '')
	mail.add_account_credentials('gmail.com', '')
	mail.add_account_credentials('outlook.com', '')
	mail.add_account_credentials('outlook.com', '')

	mail.show_server_config()
	mail.show_account_credentials()


	mail.login('gmail.com', '')

	mail.login('gmail.com', '')

	mail.login('outlook.com', '')

	mail.login('outlook.com', '')


	# CLEAN UP
	mail.logoff()

if __name__ == "__main__":
	main()