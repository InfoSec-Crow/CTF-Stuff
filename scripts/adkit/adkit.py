#!/usr/bin/python3 

import os
import subprocess
import argparse
import config
from mods import dacl, lst, enum, atk

info = '''
[Enumeration]
krb = generate krb5 file\t(nxc)
bh = collect bloodhound\t(rust-bh)
dele = find delegation\t(impacket)
mem = memberships\t(bloodyad)

[Lists]
user = usernames\t(bloodyad)
computer = computers\t(bloodyad)
group = groups\t\t(bloodyad)

[DACL]
acl = show acl\t(impacket)
gadd = add user to group\t(bloodyad)
glist = list groups from user\t(impacket)
gremove = remove user from group\t(bloodyad)

[Attacks]
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

parser.add_argument("-a", "--action", default=[], type=str, const='__show__', nargs="?", help=info)

parser.add_argument("-v", "--verbose", action="store_true", help="Show command output == terminal")
args = parser.parse_args()

#config.VERBOSE = [' > /dev/null 2>&1']
config.VERBOSE = args.verbose

box = config.Box()
box.username = args.username
box.password = args.password
box.target = args.target
box.targetgroup = args.targetgroup

print(f'''NAME:\t\t{box.name}
IP:\t\t{box.ip}
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

if args.action == '__show__':
    print(info)
    exit()
for action in args.action.split(','):
    if 'krb5' == args.action:
        enum.generate_krb5(box)
    if 'bh' == args.action:
        enum.dmp_bloodhound(box, path) 
    if 'acl' == args.action:
        enum.list_acl(box, path)
    if 'dele' == args.action:
        enum.findDelegation(box, path)
    if 'mem' == args.action:
        enum.membership(box, path)
    if 'user' == args.action:
        lst.users(box, path)
    if 'computer' == args.action:
        lst.computers(box, path)
    if 'group' == args.action:
        lst.groups(box, path)
    if 'gadd' == args.action:
        dacl.add_user_to_group(box)
    if 'glist' == args.action:
        dacl.list_user_to_group(box)
    if 'gremove' == args.action:
        dacl.remove_user_to_group(box)
    if 'aroast' == args.action:
        atk.asreproast(box, path)
    if 'kroast' == args.action:
        atk.krbroast(box, path)
    if 'tkroast' == args.action:
        atk.target_krbroast(box, path)
    if 'sc' == args.action:
        atk.shadow_creds(box, path)
    if 'gmsa' == args.action:
        atk.ReadGMSAPassword(box, path)
    if 'chpw' == args.action:
        atk.ForceChangePassword(box)

