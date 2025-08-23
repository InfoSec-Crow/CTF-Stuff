#!/usr/bin/python3
import os
import re
import subprocess
import argparse
import config, box_target, manpage
from mods import dacl, lst, enum, atk, adcs, protocol, msf

parser = argparse.ArgumentParser(
    description="Toolkit for Windows AD enumeration and exploitation",
    formatter_class=argparse.RawTextHelpFormatter,
    add_help=False
)
parser.add_argument('--help', action="store_true", help='Display all or used action info')
parser.add_argument('-h', action="help", help='Display the options/usage info')
parser.add_argument("-i", "--ip", type=str, help='Only for generate hosts file (nxc)')
parser.add_argument("-u", "--username", type=str)
parser.add_argument("-p", "--password", type=str)
parser.add_argument("-H", "--hash", nargs='?', const=True, default=False, help='Use NT hash or make on from Password')
parser.add_argument("-k", "--kerberos", nargs='?', const=True, default=False, help="Use Kerberos authentication; passing of ccache file path possible")

parser.add_argument("-t", "--target", type=str, help='If no input is made, the username is the target')
parser.add_argument("-tg", "--targetgroup", type=str.lower)
parser.add_argument("-f", "--file", type=str, help="Input file name")
parser.add_argument("-o", "--outputfile", type=str, help="Output file name")
parser.add_argument("-a", "--action", default='', type=str, const='__show__', nargs="?", help="Action to do (see --help)")
parser.add_argument("-ca", "--caname", help='The name of the CA to sign this cert')
parser.add_argument("-x", "--cmd", type=str, default='', help='Command/Query to run')
parser.add_argument("-y", "--skip", action="store_true", help='Skip user input, use DEFAULT')
parser.add_argument("-q", "--quiet", action="store_true", help="Don't show box target info")
#parser.add_argument("-v", "--verbose", action="store_true", help="Show command output == terminal")
args = parser.parse_args()

config.CWD = os.getcwd()
config.SKIP = args.skip
config.QUITE = args.quiet
if args.outputfile and "/" not in args.outputfile:
    config.OUTPUT_FILE = f"{os.getcwd()}/{args.outputfile}"
else:
    config.OUTPUT_FILE = args.outputfile
if args.ip:
    if not config.ip_in_hosts(args.ip):
        config.set_hosts_entry(args.ip)

#config.VERBOSE = [' > /dev/null 2>&1']
#config.VERBOSE = args.verbose

bad_terminal_chars = set(r"$&;|<>()[\]{}?*~`\"\\!#%^=")
if args.username and '$' in args.username: 
    args.username = f"'{args.username}'"
if args.target and '$' in args.target: 
    args.target = f"'{args.target}'"


# Init
box = box_target.Box()
box.username = args.username
box.ca = args.caname
box.file = args.file
box.target = args.target
box.targetgroup = args.targetgroup

if args.password:
    box.password = args.password
    if any(c in bad_terminal_chars for c in args.password):
        box.password = f"'{args.password}'"
if args.hash:
    if args.hash is True:
        box.nt_hash = config.nt_hashing(box.password)
    else:
        if len(args.hash) != 32:
            print("\033[91m[!]\033[0m Wrong NT hash format: 32 length")
            exit()
        if not all(c.isdigit() or ('a' <= c <= 'f') for c in args.hash):
            print("\033[91m[!]\033[0m Wrong NT hash format: only digits and lowercase letters")
            exit()
        box.nt_hash = args.hash

path = config.PATH()
path.setup(box.name)
if box.name:
    os.makedirs(path.ws, exist_ok=True)
    os.makedirs(path.ws_log, exist_ok=True)
    os.makedirs(path.ws_enum, exist_ok=True)
    os.makedirs(path.ws_lst, exist_ok=True)
    os.makedirs(path.ws_atk, exist_ok=True)
    os.makedirs(path.ws_ccache, exist_ok=True)
    os.makedirs(path.ws_adcs, exist_ok=True)
    os.makedirs(path.ws_scr, exist_ok=True)

if args.kerberos:
    config.check_krb_config(box.domain)
    box.krb = args.kerberos
    config.time_sync(box.fqdn)
    if args.kerberos is True or args.kerberos == 'set':
        ccache_path = config.kerberos_auth(box, path)
        box.krb_ccache = f"KRB5CCNAME='{ccache_path}'"
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

config.HELP = args.help
if args.help:
    print("[?] Show action infos")
    if not args.action:
        print(manpage.info)
        exit(0)
else:
    box_target.info(box)

if args.action == '__show__':
    print(manpage.info)
    exit(0)
for action in args.action.split(','):
# [Protocol]
    if 'smb' == action:
        protocol.smb_view(box,path)
    elif 'winrm' == action:
        protocol.winrm(box, path, args.cmd)
    elif 'ldap' == action:
        protocol.ldap(box, path, args.cmd)

# [Enumeration]
    elif 'krb' == action:
        enum.generate_krb(box)
    elif 'bh' == action:
        enum.dmp_bloodhound(box, path) 
    elif 'dele' == action:
        enum.findDelegation(box, path)
    elif 'sid' == action:
        enum.domain_sids(box, path)

# [Lists]
    elif 'user' == action:
        lst.users(box, path)
    elif 'computer' == action:
        lst.computers(box, path)
    elif 'group' == action:
        lst.groups(box, path)

# [DACL]
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
    elif 'wspn' == action:
        dacl.write_spn(box)
    elif 'cadd' == action:
        dacl.addcomputer(box)

# [Attack]
    elif 'aroast' == action:
        atk.asreproast(box, path)
    elif 'kroast' == action:
        atk.krbroast(box, path)
    elif 'kroast-imp' == action:
        atk.krbroast_imp(box, path)
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
    elif 'rbcd' == action:
        atk.rbcd(box,path)

# [ADCS]
    elif 'vulntemp' == action:
        adcs.find_vuln_temp(box,path)
    elif 'esc1' == action:
        adcs.esc1(box,path)
    elif 'esc2' == action or 'esc3' == action:
        adcs.esc2_and_3(box,path, action[-1])
    elif 'esc4' == action:
        adcs.esc4(box,path)

    elif 'msf' == action:
        msf.menu(box,path)
    else:
        if args.action:
            print(f'\033[91m[!]\033[0m There is no action: {action}')
            exit()
