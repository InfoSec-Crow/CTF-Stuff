#!/usr/bin/python3 

import os
import subprocess
import argparse
import re
import config
from mods import dacl, lst, enum, atk

info_enum = '''
k = generate krb5 file\t(nxc)
b = collect bloodhound\t(rust-bh)
d = find delegation\t(impacket)
mem = memberships\t(bloodyad)
'''
info_lst = '''
user = usernames\t(bloodyad)
computer = computers\t(bloodyad)
group = groups\t\t(bloodyad)
'''
info_dacl = '''
acl = show acl\t(impacket)
add = add user to group\t(impacket)
list = list groups from user\t(impacket)
remove = remove user from group\t(impacket)
'''
info_atk = '''
aroast = asreproasting\t(nxc)
kroast = kerberoasting\t(nxc)
chpw = ForceChangePassword\t(bloodyad)
sc = Shadow Credentials\t(certipy)
gmsa = ReadGMSAPassword\t(nxc)
'''

parser = argparse.ArgumentParser(
    description="Toolkit for Windows AD enumeration and exploitation",
    formatter_class=argparse.RawTextHelpFormatter
)
# parser.add_argument("-i", "--ip", type=str)
# parser.add_argument("--name", type=str.lower)
# parser.add_argument("--domain", type=str.lower)
# parser.add_argument("--fqdn", type=str.lower)
parser.add_argument("-u", "--username", type=str)
parser.add_argument("-p", "--password", type=str)
parser.add_argument("-t", "--target", type=str.lower, help='If no input is made, the username is the target')
parser.add_argument("-tg", "--targetgroup", type=str.lower)

parser.add_argument("-e", "--enum", default=[], const='__SHOW__', nargs="?", help=info_enum)
parser.add_argument("-l", "--lst", default=[], const='__SHOW__', nargs="?", help=info_lst)
parser.add_argument("-d", "--dacl", default=[], const='__SHOW__', nargs="?", help=info_dacl)
parser.add_argument("-a", "--atk", default=[], const='__SHOW__', nargs="?", help=info_atk)

parser.add_argument("-v", "--verbose", action="store_true", help="Show command output == terminal")
args = parser.parse_args()

if not args.verbose:
    config.VERBOSE = [' > /dev/null 2>&1']
else:
    config.VERBOSE = ['']

box = config.Box()
box.username = args.username
box.password = args.password
if args.target:
    box.target = args.target
else:
    box.target = args.username
box.targetgroup = args.targetgroup

print(f'''NAME:\t\t{box.name}
HOSTNAME:\t{box.hostname}
FQDN:\t\t{box.fqdn}
DOMAIN:\t\t{box.domain}
CREDS:\t\t{box.username}: {box.password}
TARGET:\t\t{box.target}
TARGET GROUP:\t{box.targetgroup}\n''')

path = config.PATH()
path.setup(box.name)
os.makedirs(path.ws, exist_ok=True)
os.makedirs(path.ws_log, exist_ok=True)
os.makedirs(path.ws_enum, exist_ok=True)
os.makedirs(path.ws_lst, exist_ok=True)
os.makedirs(path.ws_atk, exist_ok=True)

if args.enum == '__SHOW__':
    print(f'>>> Possible enumeration methods:\n{info_enum}')
    exit()
else:
    if 'k' == args.enum:
        enum.generate_krb5(box)
    if 'b' == args.enum:
        enum.dmp_bloodhound(box, path) 
    if 'acl' == args.enum:
        enum.list_acl(box, path)
    if 'd' == args.enum:
        enum.findDelegation(box, path)
    if 'mem' == args.enum:
        enum.membership(box, path)

if args.lst == '__SHOW__':
    print(f'>>> Possible list methods:\n{info_lst}')
    exit()
else:
    if 'user' == args.lst:
        lst.users(box, path)
    if 'computer' == args.lst:
        lst.computers(box, path)
    if 'group' == args.lst:
        lst.groups(box, path)

if args.dacl == '__SHOW__':
    print(f'>>> Possible dacl methods:\n{info_dacl}')
    exit()
else:
    if 'add' == args.dacl:
        dacl.add_user_to_group(box)
    if 'list' == args.dacl:
        dacl.list_user_to_group(box)
    if 'remove' == args.dacl:
        dacl.remove_user_to_group(box)

if args.atk == '__SHOW__':
    print(f'>>> Possible attack methods:\n{info_atk}')
    exit()
else:
    if 'aroast' == args.atk:
        atk.asreproast(box, path)
    if 'kroast' == args.atk:
        atk.krbroast(box, path)
    if 'sc' == args.atk:
        atk.shadow_creds(box, path)
    if 'gmsa' == args.atk:
        atk.ReadGMSAPassword(box, path)
    if 'chpw' == args.atk:
        atk.ForceChangePassword(box)

