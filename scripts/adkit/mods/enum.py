import os 
import config
import sys
import select

krb_temp = "/opt/CTF-Stuff/scripts/adkit/krb_temp.txt"

def generate_krb(box):
    if config.HELP:    
        print("""
Action:\t[Enumeration] krb
Tool:\tnetexec, none
Option:\t/
Desc:\tGenerate the /etc/krb5.conf for Kerberos authentication.
Info:\tUsing netexec sometimes creates incorrect output.
        """)
        return 0
    user_input = input("\033[94m[>]\033[0m Choose one [TEMP,nxc]: ")
    if not user_input:
        user_input = "temp"
    if user_input.lower() == "nxc":
        print('\033[93m[*]\033[0m Generate /etc/krb5.conf file (nxc)')
        cmd = f'netexec smb {box.fqdn} --generate-krb5-file /etc/krb5.conf'
        config.log_cmd(cmd)
        print(f'\033[96m[$]\033[0m {cmd}')
        os.system(cmd)
        os.system('cat /etc/krb5.conf')
        print('\033[92m[+]\033[0m Generate /etc/krb5.conf file\n')
    elif user_input.lower() == "temp":
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
    else:
        print("\033[91m[!]\033[0m Incorrect input!")
        exit()

def dmp_bloodhound(box, path):
    if config.HELP:    
        print("""
Action:\t[Enumeration] bh
Tool:\tbloodhound-python, rusthound-ce
Option:\t-u, --username
\t-p --password; -H, --hash; -k
Desc:\tCollects data for BloodHound CE.
Info:\tTool rusthound-ce don't support NT hash auth.
        """)
        return 0
    user_input = input("\033[94m[>]\033[0m Choose one [PY,rust]: ")
    if not user_input:
        user_input = "py"
    if user_input.lower() == "py":
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
    elif user_input.lower() == "rust":
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
    else:
        print("\033[91m[!]\033[0m Incorrect input!")
        exit()

def findDelegation(box, path):
    if config.HELP:    
        print("""
Action:\t[Enumeration] dele
Tool:\timpacket
Option:\t-u, --username
\t-p --password; -H, --hash; -k
Desc:\tList all delegation relationships.
Info:\t/
        """)
        return 0
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
    if config.HELP:    
        print("""
Action:\t[Enumeration] sid
Tool:\timpacket
Option:\t-u, --username
\t-p --password; -H, --hash; -k
Desc:\tSID brute forcer example through [MS-LSAT] MSRPC Interface, save output to a file.
Info:\t/
        """)
        return 0
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