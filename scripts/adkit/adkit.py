#!/usr/bin/python3 

import os
import re
import subprocess
import argparse
import config
from mods import dacl, lst, enum, atk, adcs

info = '''
[Enumeration]
krb = generate krb5 file\t(template)
krb-nxc = generate krb5 file\t(nxc)
bh-rust = collect bloodhound\t(rust-bh)
bh-py = collect bloodhound\t(python-bh)
smb = view smb shares and files\t(nxc,impacket)
dele = find delegation\t(impacket)
sid = domain sids\t(impacket)

[Lists]
user = list all usernames\t(bloodyad)
computer = list all computers\t(bloodyad)
group = list all groups\t\t(bloodyad)

[DACL]
acl = show acl\t(impacket)
gadd = add user to group\t(bloodyad)
glist = list groups from user\t(bloodyad)
gremove = remove user from group\t(bloodyad)
edit = set dacl FullControl\t(impacket)
active = activate account\t(bloodyad)
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
esc1 = ESC1\t(certipy)
esc2 = ESC2\t(certipy)
esc3 = ESC3\t(certipy)
esc4 = ESC4\t(certipy)
'''

parser = argparse.ArgumentParser(
    description="Toolkit for Windows AD enumeration and exploitation",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("-i", "--ip", type=str, help='Only for generate hosts file (nxc)')
parser.add_argument("--ldap", action="store_true", help='Generate hosts file via LDAP (nmap)')
parser.add_argument("-u", "--username", type=str)
parser.add_argument("-p", "--password", type=str)
parser.add_argument("-H", "--hash", nargs='?', const=True, default=False, help='Use NT hash or make on from Password')
parser.add_argument("-k", "--kerberos", nargs='?', const=True, default=False, help="Use Kerberos authentication; passing of ccache file path possible")

parser.add_argument("-t", "--target", type=str.lower, help='If no input is made, the username is the target')
parser.add_argument("-tg", "--targetgroup", type=str.lower)
parser.add_argument("-a", "--action", default='', type=str, const='__show__', nargs="?", help=info)
parser.add_argument("-ca", "--caname", help='The name of the CA to sign this cert')

#parser.add_argument("-v", "--verbose", action="store_true", help="Show command output == terminal")
args = parser.parse_args()

if args.ip:
    if args.ldap:
        config.set_hosts_entry_ldap(args.ip)
    else:
        config.set_hosts_entry(args.ip)

#config.VERBOSE = [' > /dev/null 2>&1']
#config.VERBOSE = args.verbose
bad_terminal_chars = set(r"$&;|<>()[\]{}?*~`\"\\!#%^=")
if args.username and '$' in args.username: 
    args.username = f"'{args.username}'"
if args.target and '$' in args.target: 
    args.target = f"'{args.target}'"

password = None
optional_target = ""
box = config.Box()
box.username = args.username
box.ca = args.caname
if not box.target:
    optional_target = f"({box.username})"
box.target = args.target
box.targetgroup = args.targetgroup

if args.password:
    box.password = args.password
    if any(c in bad_terminal_chars for c in args.password):
        box.password = f"'{args.password}'"
    password = args.password
if args.hash:
    if args.hash is True:
        box.nt_hash = config.nt_hashing(box, args.hash)
        password = box.nt_hash
    else:
        if len(args.hash) != 32:
            print("\033[91m[!]\033[0m Wrong NT hash format: 32 length")
            exit()
        if not all(c.isdigit() or ('a' <= c <= 'f') for c in args.hash):
            print("\033[91m[!]\033[0m Wrong NT hash format: only digits and lowercase letters")
            exit()
        box.nt_hash = args.hash
        password = box.nt_hash

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
    box.krb = args.kerberos
    os.system(f'sudo ntpdate {box.fqdn} > /dev/null 2>&1')
    if args.kerberos is True or args.kerberos == 'set':
        box.krb_ccache = config.kerberos_auth(box, path)
    else:
        pwd = ""
        if '/' not in args.kerberos:
            pwd = os.getcwd() + "/"
        ccache_path = pwd+args.kerberos
        if not os.path.exists(ccache_path):
            print(f"\033[91m[!]\033[0m File {ccache_path} not exists")
            exit()
        box.krb_ccache = f"KRB5CCNAME='{ccache_path}'"
    if box.nt_hash:
        box.krb = ccache_path

print(f'''NAME:\t\t{box.name}
IP:\t\t{box.ip}
HOSTNAME:\t{box.hostname}
FQDN:\t\t{box.fqdn}
DOMAIN:\t\t{box.domain}
CREDS:\t\t{box.username} : {password}
CACHE:\t\t{krb}
TARGET:\t\t{box.target} {optional_target}
TARGET GROUP:\t{box.targetgroup}\n''')

if args.action == '__show__':
    print(info)
    exit()
for action in args.action.split(','):
    if 'krb' == action:
        enum.generate_krb5(box)
    elif 'krb-exc' == action:
        enum.generate_krb5_nxc(box)
    elif 'bh-rust' == action:
        enum.dmp_bloodhound_rust(box, path) 
    elif 'bh-py' == action:
        enum.dmp_bloodhound_python(box, path) 
    elif 'dele' == action:
        enum.findDelegation(box, path)
    elif 'sid' == action:
        enum.domain_sids(box, path)
    elif 'smb' == action:
        enum.smb_view(box,path)

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
    elif 'active' == action:
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
    elif 'esc1' == action:
        adcs.esc1(box,path)
    elif 'esc2' == action or 'esc3' == action:
        adcs.esc2_and_3(box,path, action[-1])
    elif 'esc4' == action:
        adcs.esc4(box,path)


    else:
        print(f'\033[91m[!]\033[0m There is no action: {action}')
        exit()
