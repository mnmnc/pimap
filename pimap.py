
import imaplib

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

