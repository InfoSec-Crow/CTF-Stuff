import os 
import config

def generate_krb5(box):
    print('\033[93m[*]\033[0m Generate /etc/krb5.conf file')
    cmd = f'netexec smb {box.fqdn} --generate-krb5-file /etc/krb5.conf'
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    os.system('cat /etc/krb5.conf')
    print('\033[92m[+]\033[0m Generate /etc/krb5.conf file\n')

def dmp_bloodhound(box, path):
    config.required_creds(box)
    print('\033[93m[*]\033[0m Dump BloodHound data')
    if box.nt_hash or box.krb:
        print('[!] No NT-hash support, use kerberos authentication!')
        print('[!] Need /etc/krb5.conf file, use -a, --action krb')
        krb = config.kerberos_auth(box, path)
        cmd = f"{krb} rusthound-ce -f {box.fqdn} -d {box.domain} -n {box.ip} -u {box.username} -k -c All --zip"
    else:
        cmd = f"rusthound-ce -f {box.fqdn} -d {box.domain} -n {box.ip} -u {box.username} -p '{box.password}' -c All --zip"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.chdir(path.ws_enum)
    os.system(cmd+ ' 2>&1 | tee dump_bloodhound.out')
    print('\033[92m[+]\033[0m Dump BloodHound data\n')
    
def findDelegation(box, path):
    config.required_creds(box)
    os.chdir(path.ws_enum)
    print('\033[93m[*]\033[0m Find Delegation')
    if box.krb:
        cmd = f"{box.krb} impacket-findDelegation {box.domain}/{box.username} -k -no-pass"
    elif box.nt_hash:
        cmd = f"impacket-findDelegation {box.domain}/{box.username} -hashes :{box.nt_hash}"
    else:
        cmd = f"impacket-findDelegation {box.domain}/{box.username}:'{box.password}'"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m Find Delegation\n')

def domain_sids(box, path):
    config.required_creds(box)
    os.chdir(path.ws_enum)
    print('\033[93m[*]\033[0m Domain SIDs')
    if box.krb:
        cmd = f"{box.krb} impacket-lookupsid {box.domain}/{box.username}@{box.fqdn} -k -no-pass -domain-sids"
    elif box.nt_hash:
        cmd = f"impacket-lookupsid {box.domain}/{box.username}@{box.fqdn} -hashes :{box.nt_hash} -domain-sids"
    else:
        cmd = f"impacket-lookupsid {box.domain}/{box.username}:'{box.password}'@{box.fqdn} -domain-sids"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+ ' 2>&1 | tee domain-sids.out')
    print('\033[92m[+]\033[0m Domain SIDs\n')