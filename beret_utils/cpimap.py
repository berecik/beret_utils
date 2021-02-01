'''
Created on 2010-08-20

@author: beret
'''

# !/usr/bin/env python

import imaplib
import sys


def cpimap(user1, host1, pass1, user2, host2, pass2, target='/'):
    m1 = imaplib.IMAP4_SSL(host1)
    m2 = imaplib.IMAP4_SSL(host2)
    m1.login(user1, pass1)
    m2.login(user2, pass2)

    folders = [folder.split(' "/" ')[1][1:-1] for folder in filter(lambda x: x, m1.list()[1])]
    folders2 = [folder.split(' "/" ')[1][1:-1] for folder in filter(lambda x: x, m2.list()[1])]
    #    folders.insert( 0, target ) # Copy messages in the root of the target too

    print('Copying', len(folders), 'folders:')
    for f in folders:
        print(f)

    for f in folders:
        if '\\' in f:
            print('Skipping', f)
            # imaplib does not support backslashes in mailbox names!
            continue
        print('Copying', f)
        if f not in folders2:
            m2.create(f)
        m1.select(f)
        print('Fetching messages...')
        typ, data = m1.search(None, 'ALL')

        msgs = data[0].split()

        sys.stdout.write(" ".join(['Copying', str(len(msgs)), 'messages']))

        for num in msgs:
            typ, data = m1.fetch(num, '(RFC822)')
            sys.stdout.write('.')
            m2.append(f, None, None, data[0][1])
        sys.stdout.write('\n')


if __name__ == '__main__':
    user1 = 'test'
    host1 = 'test.ceenet.org'
    pass1 = 'test'
    user2 = 'test@hipisi.org.pl'
    host2 = 'imap.gmail.com'
    pass2 = 'test'
    cpimap(user1, host1, pass1, user2, host2, pass2)
