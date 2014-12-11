Total Commander FTP Password Recovery Tool
==========================================
Simple Python script, which can recover Total Commander stored FTP passwords.

Usage
=====

```
tcpwrecovery.py [options]

Options:
  -h, --help            show this help message and exit
  -c, --common          Search wcx_ftp.ini in common places
  -f FILE, --file=FILE  File to decrypt
  -p PASSWORD, --password=PASSWORD
                        Password to decrypt
```
It can search in some common places for the INI file, you can explicitly specify the location or you can simply supply the encrypted password. Sample output:

```
c:\tcpwrecovery>tcpwrecovery.py -c
-> Trying: C:\Users\user1\AppData\Roaming\GHISLER\wcx_ftp.ini
-> Found: C:\Users\user1\AppData\Roaming\GHISLER\wcx_ftp.ini
-> Decrypting: C:\Users\user1\AppData\Roaming\GHISLER\wcx_ftp.ini

[connections]
1=example.com
default=example.com
[example.com]
host=example.com
username=fakeusername
password=fakepassword
pasvmode=0
MLSD=-1
[default]
pasvmode=0

-> Trying: C:\Windows\wcx_ftp.ini
-> Not found: C:\Windows\wcx_ftp.ini

-> Trying: wcx_ftp.ini
-> Not found: wcx_ftp.ini
```