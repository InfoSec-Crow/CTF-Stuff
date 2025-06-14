#!/usr/bin/python3 

import os
import subprocess
import argparse
import config
from mods import dacl, lst, enum, atk, adcs

info = '''
[Enumeration]
krb = generate krb5 file\t(nxc)
bh = collect bloodhound\t(rust-bh)
dele = find delegation\t(impacket)
sid = domain sids\t(impacket)

[Lists]
user = usernames\t(bloodyad)
computer = computers\t(bloodyad)
group = groups\t\t(bloodyad)

[DACL]
acl = show acl\t(impacket)
gadd = add user to group\t(bloodyad)
glist = list groups from user\t(bloodyad)
gremove = remove user from group\t(bloodyad)
activ = activate account\t(bloodyad)
wowner = write owner\t(impacket)
rowner = read owner\t(impacket)

[Attacks]
aroast = asreproasting\t(nxc)
kroast = kerberoasting\t(nxc)
chpw = ForceChangePassword\t(bloodyad)
sc = Shadow Credentials\t(certipy)
gmsa = ReadGMSAPassword\t(nxc)
laps = ReadLAPSPassword\t(impacket)
dcsync = DCSync\t(impacket)
gold = Golden Ticket\t(impacket)
silver = Silver Ticket\t(impacket)

[ADCS]
vulntemp = find vuln CertTemp\t(certipy)
'''

parser = argparse.ArgumentParser(
    description="Toolkit for Windows AD enumeration and exploitation",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("-i", "--ip", type=str, help='Only for generate hosts file')
# parser.add_argument("--name", type=str.lower)
# parser.add_argument("--domain", type=str.lower)
# parser.add_argument("--fqdn", type=str.lower)
parser.add_argument("-u", "--username", type=str)
parser.add_argument("-p", "--password", type=str)
parser.add_argument("-H", "--hash", type=str, nargs='?', const='empty', help='users NT hash')
parser.add_argument("-k", "--kerberos", nargs='?', const=True, default=False, help="Use Kerberos authentication; passing of ccache file path possible")

parser.add_argument("-t", "--target", type=str.lower, help='If no input is made, the username is the target')
parser.add_argument("-tg", "--targetgroup", type=str.lower)
parser.add_argument("-a", "--action", default=[], type=str, const='__show__', nargs="?", help=info)

#parser.add_argument("-v", "--verbose", action="store_true", help="Show command output == terminal")

args = parser.parse_args()

if args.ip:
    config.set_hosts_entry(args.ip)
    exit()

#config.VERBOSE = [' > /dev/null 2>&1']
#config.VERBOSE = args.verbose

password = None
box = config.Box()
box.username = args.username
if args.password:
    box.password = args.password
    password = args.password
if args.hash == 'empty':
    box.nt_hash = config.nt_hashing(box, args.hash)
    password = box.nt_hash
elif args.hash:
    box.nt_hash = args.hash
    password = box.nt_hash
box.target = args.target
box.targetgroup = args.targetgroup

path = config.PATH()
path.setup(box.name)
os.makedirs(path.ws, exist_ok=True)
os.makedirs(path.ws_log, exist_ok=True)
os.makedirs(path.ws_enum, exist_ok=True)
os.makedirs(path.ws_lst, exist_ok=True)
os.makedirs(path.ws_atk, exist_ok=True)
os.makedirs(path.ws_ccache, exist_ok=True)
os.makedirs(path.ws_adcs, exist_ok=True)

if args.kerberos:
    os.system(f'sudo ntpdate {box.fqdn} > /dev/null 2>&1')
    if args.kerberos == True:
        box.krb = config.kerberos_auth(box, path)
    elif '/' in args.kerberos:
        box.krb = f"KRB5CCNAME='{args.kerberos}'"
    else:
        box.krb = f"KRB5CCNAME='{path.ws_ccache}{args.kerberos}'"

print(f'''NAME:\t\t{box.name}
IP:\t\t{box.ip}
HOSTNAME:\t{box.hostname}
FQDN:\t\t{box.fqdn}
DOMAIN:\t\t{box.domain}
CREDS:\t\t{box.username} : {password}
CACHE:\t\t{box.krb}
TARGET:\t\t{box.target}
TARGET GROUP:\t{box.targetgroup}\n''')

if args.action == '__show__':
    print(info)
    exit()
for action in args.action.split(','):
    if 'krb' == action:
        enum.generate_krb5(box)
    elif 'bh' == action:
        enum.dmp_bloodhound(box, path) 
    elif 'dele' == action:
        enum.findDelegation(box, path)
    elif 'sid' == action:
        enum.domain_sids(box, path)

    elif 'user' == action:
        lst.users(box, path)
    elif 'computer' == action:
        lst.computers(box, path)
    elif 'group' == action:
        lst.groups(box, path)

    elif 'acl' == action:
        dacl.list_acl(box, path)
    elif 'gadd' == action:
        dacl.add_user_to_group(box)
    elif 'glist' == action:
        dacl.list_user_to_group(box)
    elif 'gremove' == action:
        dacl.remove_user_to_group(box)
    elif 'activ' == action:
        dacl.activate_account(box)
    elif 'wowner' == action:
        dacl.read_write_owner(box, 'write')
    elif 'rowner' == action:
        dacl.read_write_owner(box, 'read')
    elif 'edit' == action:
        dacl.dacledit(box)

    elif 'aroast' == action:
        atk.asreproast(box, path)
    elif 'kroast' == action:
        atk.krbroast(box, path)
    elif 'tkroast' == action:
        atk.target_krbroast(box, path)
    elif 'sc' == action:
        atk.shadow_creds(box, path)
    elif 'gmsa' == action:
        atk.ReadGMSAPassword(box, path)
    elif 'laps' == action:
        atk.ReadLAPSPassword(box, path)
    elif 'chpw' == action:
        atk.ForceChangePassword(box)
    elif 'dcsync' == action:
        atk.dcsync(box,path)
    elif 'gold' == action:
        atk.golden_ticket(box,path)  
    elif 'silver' == action:
        atk.silver_ticket(box,path) 
    elif 'vulntemp' == action:
        adcs.find_vuln_temp(box,path)

    else:
        print(f'\033[91m[!]\033[0m There is no action: {action}')
        exit()
