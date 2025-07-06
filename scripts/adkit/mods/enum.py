import os 
import config

krb_temp = "/opt/CTF-Stuff/scripts/adkit/krb_temp.txt"

def generate_krb5_nxc(box):
    print('\033[93m[*]\033[0m Generate /etc/krb5.conf file (nxc)')
    cmd = f'netexec smb {box.fqdn} --generate-krb5-file /etc/krb5.conf'
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    os.system('cat /etc/krb5.conf')
    print('\033[92m[+]\033[0m Generate /etc/krb5.conf file\n')

def generate_krb5(box):
    print('\033[93m[*]\033[0m Generate /etc/krb5.conf file (from template)')
    with open(krb_temp, "r") as f:
        content = f.read()
    content = content.replace("<DOMAIN>", box.domain.upper())
    content = content.replace("<domain>", box.domain)
    content = content.replace("<fqdn>", box.fqdn)
    with open("/etc/krb5.conf", "w") as f:
        f.write(content)
    os.system('cat /etc/krb5.conf')
    print('\n\033[92m[+]\033[0m Generate /etc/krb5.conf file\n')

def smb_view(box, path):
    config.required_creds(box)
    os.chdir(path.ws_enum)
    print('\033[93m[*]\033[0m List SMB shares & files')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} netexec smb {box.fqdn} --use-kcache --shares"
        cmd2 = f"{box.krb_ccache} netexec smb {box.fqdn} --use-kcache -M spider_plus"
        cmd3 = f"{box.krb_ccache} impacket-smbclient -k -no-pass {box.fqdn}"
    elif box.krb:
        cmd = f"netexec smb {box.fqdn} -u {box.username} -p {box.password} -k --shares"
        cmd2 = f"netexec smb {box.fqdn} -u {box.username} -p {box.password} -k -M spider_plus"
        cmd3 = f"impacket-smbclient -k {box.domain}/{box.username}:{box.password}@{box.fqdn}"
    elif box.nt_hash:
        cmd = f"netexec smb {box.fqdn} -u {box.username} -H {box.nt_hash} --shares"
        cmd2 = f"netexec smb {box.fqdn} -u {box.username} -H {box.nt_hash} -M spider_plus"
        cmd3 = f"impacket-smbclient {box.domain}/{box.username}@{box.fqdn} -hashes :{box.nt_hash}"
    else:
        cmd = f"netexec smb {box.fqdn} -u {box.username} -p {box.password} --shares"
        cmd2 = f"netexec smb {box.fqdn} -u {box.username} -p {box.password} -M spider_plus"
        cmd3 = f"impacket-smbclient {box.domain}/{box.username}:{box.password}@{box.fqdn}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    filter = " | awk '/Share/ {f=1} f' | sed 's/^SMB.*"+box.hostname+"[[:space:]]\\+//'"
    os.system(cmd+filter+f' | tee {box.username}_smb-shares.txt')
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    out = os.popen(cmd2).read()
    print('\n'.join(out.splitlines()[-10:]))
    os.system(f'cp /home/kali/.nxc/modules/nxc_spider_plus/{box.fqdn}.json .')
    print(f'[*] Output file: /home/kali/.nxc/modules/nxc_spider_plus/{box.fqdn}.json')
    print(f'\n\033[96m[$]\033[0m {cmd3}')
    print('\033[92m[+]\033[0m List SMB shares\n')

def dmp_bloodhound_python(box, path):
    config.required_creds(box)
    print('\033[93m[*]\033[0m Dump BloodHound data (python)')
    if isinstance(box.krb, str):
        username = box.username
        if not box.username:
            print("[!] Username is required for Kerberos ccache authentication")
            username = box.krb_ccache.split('/')[-1].split('.ccache')[0]
            print(f"[!] Use username: {username} from ccache file")
        cmd = f"{box.krb_ccache} bloodhound-python -k -no-pass -u '{username}' -d {box.domain} -ns {box.ip} -c ALl --zip -op python"
    elif box.krb:
        cmd = f"bloodhound-python -u {box.username} -p {box.password} -k -d {box.domain} -ns {box.ip} -c ALl --zip -op python"
    elif box.nt_hash:
        cmd = f"bloodhound-python -u {box.username} --hashes {box.nt_hash} -d {box.domain} -ns {box.ip} -c ALl --zip -op python"
    else:
        cmd = f"bloodhound-python -u {box.username} -p {box.password} -d {box.domain} -ns {box.ip} -c ALl --zip -op python"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.chdir(path.ws_enum)
    os.system(cmd+ ' 2>&1 | tee dump_bloodhound_python.out')
    print('\033[92m[+]\033[0m Dump BloodHound data\n')

def dmp_bloodhound_rust(box, path):
    config.required_creds(box)
    print('\033[93m[*]\033[0m Dump BloodHound data (rust)')
    if isinstance(box.krb, str) or box.krb:
        cmd = f"{box.krb_ccache} rusthound-ce -f {box.fqdn} -d {box.domain} -n {box.ip} -k -c All --zip"
    elif box.nt_hash:
        print('[!] No NT-hash support, use kerberos authentication!')
        cmd = f"{config.kerberos_auth(box, path)} rusthound-ce -f {box.fqdn} -d {box.domain} -n {box.ip} -k -c All --zip"
    else:
        cmd = f"rusthound-ce -f {box.fqdn} -d {box.domain} -n {box.ip} -u {box.username} -p {box.password} -c All --zip"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.chdir(path.ws_enum)
    os.system(cmd+ ' 2>&1 | tee dump_bloodhound_rust.out')
    print('\033[92m[+]\033[0m Dump BloodHound data\n')
    
def findDelegation(box, path):
    config.required_creds(box)
    os.chdir(path.ws_enum)
    print('\033[93m[*]\033[0m Find Delegation')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} impacket-findDelegation -k -no-pass -dc-host {box.fqdn} {box.domain}/"
    elif box.krb:
        cmd = f"impacket-findDelegation -k -dc-host {box.fqdn} {box.domain}/{box.username}:{box.password}"
    elif box.nt_hash:
        cmd = f"impacket-findDelegation {box.domain}/{box.username} -hashes :{box.nt_hash}"
    else:
        cmd = f"impacket-findDelegation {box.domain}/{box.username}:{box.password}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m Find Delegation\n')

def domain_sids(box, path):
    config.required_creds(box)
    os.chdir(path.ws_enum)
    print('\033[93m[*]\033[0m Domain SIDs')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} impacket-lookupsid -k -no-pass -domain-sids {box.domain}/@{box.fqdn}"
    elif box.krb:
        cmd = f"impacket-lookupsid {box.domain}/{box.username}:{box.password}@{box.fqdn} -k -domain-sids"
    elif box.nt_hash:
        cmd = f"impacket-lookupsid {box.domain}/{box.username}@{box.fqdn} -hashes :{box.nt_hash} -domain-sids"
    else:
        cmd = f"impacket-lookupsid {box.domain}/{box.username}:{box.password}@{box.fqdn} -domain-sids"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+ ' 2>&1 | tee domain-sids.out')
    print('\033[92m[+]\033[0m Domain SIDs\n')