"""
Copyright (C) <2013> <Csaba Fitzl>
Copyright (C) <2026> <DavideDG> for the Python3 porting

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import argparse

RANDOM_BASE = 0


def process_file(filename):
    try:
        print("-> Trying: " + filename)
        f = open(filename, "r", encoding="utf-8", errors="replace")
        print("-> Found: " + filename)
        print("-> Decrypting: " + filename)
        print("")
        for line in f:
            stripped = line.strip()
            if "password" in stripped:
                print("password=" + tc_decrypt(stripped.split("=")[1]))
            else:
                print(stripped)
        f.close()
        print("")
    except IOError:
        print("-> Not found: " + filename)
        print("")


def search_ini():
    """
    Search the wcx_ftp.ini file in common places
    """
    folder = []
    folder.append(os.getenv('APPDATA') + "\\GHISLER\\wcx_ftp.ini")
    folder.append(os.getenv('SYSTEMROOT') + "\\wcx_ftp.ini")
    folder.append("wcx_ftp.ini")
    for ini in folder:
        process_file(ini)


def tc_random(nMax):
    global RANDOM_BASE
    RANDOM_BASE = ((RANDOM_BASE * 0x8088405) & 0xffffffff) + 1
    return (((RANDOM_BASE * nMax) >> 32) & 0xffffffff)


def tc_shift(n1, n2):
    return (((n1 << n2) & 0xffffffff) | ((n1 >> (8 - n2)) & 0xffffffff)) & 0xff


def tc_decrypt(pwd):
    global RANDOM_BASE
    password = []
    for i in range(len(pwd) // 2 - 4):  # skip last 8 characters (4 * 2 bytes)
        password.append(int(pwd[2 * i:2 * (i + 1)], 16))
    pwlen = len(password)

    RANDOM_BASE = 849521
    for i in range(pwlen):
        password[i] = tc_shift(password[i], tc_random(8))

    RANDOM_BASE = 12345
    for i in range(256):
        a = tc_random(pwlen)
        b = tc_random(pwlen)
        password[a], password[b] = password[b], password[a]

    RANDOM_BASE = 42340
    for i in range(pwlen):
        password[i] = (password[i] ^ tc_random(256)) & 0xff

    RANDOM_BASE = 54321
    for i in range(pwlen):
        password[i] = (password[i] - tc_random(256)) & 0xff

    for i in range(pwlen):
        password[i] = chr(password[i])

    return "".join(password)


def main():
    parser = argparse.ArgumentParser(description="Total Commander FTP password recovery")
    parser.add_argument('-c', '--common', action='store_true', default=False,
                        help='Search wcx_ftp.ini in common places')
    parser.add_argument('-f', '--file', dest='file', default='',
                        help='File to decrypt')
    parser.add_argument('-p', '--password', dest='password', default='',
                        help='Password to decrypt')
    options = parser.parse_args()

    if options.common:
        search_ini()
    if options.file != "":
        process_file(options.file)
    if options.password != "":
        pw = tc_decrypt(options.password)
        print("Decrypted password: " + pw)
    if options.file == "" and options.password == "" and not options.common:
        print('Nothing specified, run "tcpwrecovery -h" for options')


if __name__ == '__main__':
    main()
