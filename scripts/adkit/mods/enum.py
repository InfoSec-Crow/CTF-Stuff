import os 
import config

def generate_krb5(box):
    print('\033[93m[*]\033[0m Generate /etc/krb5.conf file')
    cmd = f'netexec smb {box.fqdn} --generate-krb5-file /etc/krb5.conf'
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    os.system('cat /etc/krb5.conf')
    print('\033[92m[+]\033[0m Generate /etc/krb5.conf file')

def dmp_bloodhound(box, path):
    os.chdir(path.ws_enum)
    print('\033[93m[*]\033[0m Dump BloodHound data')
    cmd = f"rusthound-ce -c All --zip -f {box.fqdn} -d {box.domain} -n IP -u {box.username} -p '{box.password}'"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd + ' 2>&1 | tee dump_bloodhound.out')
    print('\033[92m[+]\033[0m Dump BloodHound data')
    
def findDelegation(box, path):
    os.chdir(path.ws_enum)
    print('\033[93m[*]\033[0m Find Delegation')
    cmd = f"impacket-findDelegation {box.domain}/{box.username}:'{box.password}'"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m Find Delegation')

def membership(box, path):
    os.chdir(path.ws_enum)
    print(f'\033[93m[*]\033[0m Memberships')
    cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p '{box.password}' get membership {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd + f' 2>&1 | tee membership_{box.target}.out')
    print('\033[92m[+]\033[0m Memberships')

def list_acl(box, path):
    os.chdir(path.ws_enum)
    print('\033[93m[*]\033[0m List ACL')
    cmd = f"impacket-dacledit {box.domain}/{box.username}:'{box.password}' -target {box.target} -principal {box.username}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd + f' 2>&1 | tee acl_{box.username}_to_{box.target}.out')
    print('\033[92m[+]\033[0m List ACL')