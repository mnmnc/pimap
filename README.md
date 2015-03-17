# pimap
imap email automation with python


This script will (eventually) connect to designated IMAP servers (GMAIL.com, GMX.com, OUTLOOK.com) with configured accounts, *check for unread emails*, get some details about them (including headers) and show all of this in a nice form (possibly ncurses - TBD).

Example output without debug info:

```ruby
[ INP ] Password for mail1@gmail.com        :
[ INP ] Password for mail2@gmail.com        :
[ INP ] Password for mail3@gmail.com        :
[ INP ] Password for mail4@gmail.co         :
[ INP ] Password for mail5@outlook.com      :
[ INP ] Password for mail6@outlook.com      :
[ INP ] Password for mail7@outlook.com      :

----------- 2015-03-17 16:49:32.085956 -----------
[ NFO ] mail1@gmail.com / Inbox             0/148
[ NFO ] mail2@gmail.com / Inbox             1/229
[ NFO ] mail3@gmail.com / Inbox             0/39
[ NFO ] mail4@gmail.com / Inbox             0/773
[ NFO ] mail5@outlook.com / Inbox           0/0
[ NFO ] mail6@outlook.com / Inbox           0/0
[ NFO ] mail7@outlook.com / Inbox           2/2
----------- 2015-03-17 16:50:17.104958 -----------
[ NFO ] mail1@gmail.com / Inbox             0/148
[ NFO ] mail2@gmail.com / Inbox             1/229
[ NFO ] mail3@gmail.com / Inbox             0/39
[ NFO ] mail4@gmail.com / Inbox             0/773
[ NFO ] mail5@outlook.com / Inbox           0/0
[ NFO ] mail6@outlook.com / Inbox           0/0
[ NFO ] mail7@outlook.com / Inbox           2/2

```
