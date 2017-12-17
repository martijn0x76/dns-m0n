#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    dns-m0n
#
#    Copyright (C) 2017  @martijn0x76
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; Applies version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

__version__ = '1.0.1'
__author__ = '@martijn0x76'

import socket
import sqlite3
import datetime
from colorama import init, Fore, Back
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# In this file you can add the names to check / each line a name ending with a return
list = 'names.txt'

# Leave empty to disable e-mail alerts / always use host:port
mailhost = ''

mm = MIMEMultipart('alternative')
mm['Subject'] = 'dns-m0n alert'

# Set this to meet your settings
# Don't forget to uncomment the login line in sendalert() for SMTP authentication
mm['From'] = 'alert@domain.tld'
mm['To'] = 'security@domain.tld'

# Lookup results are saved in a SQLite DB
db = sqlite3.connect('dns-m0n_db')
cursor = db.cursor()

# Colorama init
init(autoreset=True)

changed = 0


# E-mail alerting
def sendalert(msg):
    if not mailhost:
        return
    else:
        c = mailhost.split(':')
        server = smtplib.SMTP(c[0], c[1])
        server.ehlo()
        server.starttls()
        server.ehlo()  # Extra ehlo required after STARTTLS..

        # Uncomment this line below if you need SMTP sender authentication
        # server.login('user@domain.tld','pass')

        part = MIMEText(msg, 'plain')
        mm.attach(part)
        server.sendmail(mm['From'], mm['To'], mm.as_string())

        server.quit()


# Main routine
print('dns-m0n by @martijn0x76 - Keeps an eye on your DNS records\n')

with open(list, 'r') as n:
    for name in n:
        nn = name.replace('\n', '')
        print('Checking: %s' % nn.ljust(20)),
        # Get current IP
        addr = socket.gethostbyname(nn)
        print('| Current: %s,' % addr),
        cursor.execute('''SELECT id FROM names WHERE Name=?''', (nn,))
        id = cursor.fetchone()
        if id is None:
            # New name found in list -> add to db
            cursor.execute('''INSERT INTO names(Name, IP, IP_OLD, Changed) 
                VALUES(?,?,?,?)''', (nn, addr, addr, datetime.datetime.now()))
            print('Before: ' + Fore.GREEN + 'new')
        else:
            # Found! Get the saved IP..
            cursor.execute('''SELECT IP FROM names WHERE id=?''', (id[0],))
            ip = cursor.fetchone()
            print('Before: %s' % ip[0]),
            # Compare current with before
            if ip[0] != addr:
                # Not equal - alarm!
                print(Fore.WHITE + Back.RED + '>>modified<<')
                cursor.execute('''UPDATE names SET IP=?, IP_OLD=?, Changed=? WHERE id=?''',
                               (addr, ip[0], datetime.datetime.now(), id[0]))
                changed += 1
                msg = '%s (%s -> %s)' % (nn, ip[0], addr)
                sendalert(msg)
            else:
                # The sound of silence..
                print('')

# Flush & close SQLite
db.commit()
db.close()

if changed > 0:
    print('\nNumber of detected changes: %d' % changed)
