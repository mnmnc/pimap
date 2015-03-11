# pimap
imap email automation with python


This script will (eventually) connect to designated IMAP servers (GMAIL.com, GMX.com, OUTLOOK.com) with configured accounts, *check for unread emails*, get some details about them (including headers) and show all of this in a nice form (possibly ncurses - TBD).

Example output so far ([316b60142a](https://github.com/mnmnc/pimap/commit/316b60142a46f27b92aa074ec04ac9f2af68a175)):

```ruby
D:\Prv\Git\pimap>python pimap.py

Getting passwords
  Password for mail1@gmail.com:
  Password for mail2@gmail.com:
  Password for mail1@outlook.com:
  Password for mail2@outlook.com:

Showing available configuration
  outlook.com      imap-mail.outlook.com:993
  gmail.com        imap.gmail.com:993

Showing available accounts configuration
outlook.com
         mail1:xxxx
         mail2:xxxx
gmail.com
         mail1:xxxx
         mail2:xxxx
         
Connecting to servers and logon attemps:       
  Logon successful.
  Logon successful.
  Logon successful.
  Logon successful.
```
