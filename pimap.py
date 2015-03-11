
import imaplib
import email

class Mail():

	def __init__(self):
		self.server_configurations = {}
		self.email_credentials = {}


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
		:param domain:
		:return:
		"""
		if domain == "ALL":
			for server_domain in self.server_configurations.keys():
				print(server_domain, '\t', self.server_configurations[server_domain][0], self.server_configurations[server_domain][0])
		else:
			if domain in self.server_configurations.keys():
				print(domain, '\t', self.server_configurations[domain][0], self.server_configurations[domain][0])
			else:
				print("[ e ] No configuration for domain:", domain)


def main():

	mail = Mail()
	mail.add_server_config('gmail.com', 'imap.gmail.com')

	pass

if __name__ == "__main__":
	main()