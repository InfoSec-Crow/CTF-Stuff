import os
import config

def users(box, path):
    if config.HELP:    
        print("""
Action:\t[Lists] user
Tool:\tbloodyAD
Option:\t-u, --username
\t-p --password; -H, --hash; -k
Desc:\tLists all users and saves them in the file user.lst
Info:\t/
        """)
        return 0
    config.required_creds(box)
    os.chdir(path.ws_lst)
    print('\033[92m[*]\033[0m List Domain Users')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} bloodyAD --host {box.fqdn} -d {box.domain} -k get children --otype user"
    elif box.krb:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} -k get children --otype user"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} get children --otype user"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} get children --otype user"
    cmd = cmd+ """ | awk -F'CN=' '{split($2,a,","); print a[1]}' | sed '/^$/d'"""
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+ ' 2>&1 | tee user.lst')
    print('\033[38;5;28m[+]\033[0m List Domain Users\n')

def computers(box, path):
    if config.HELP:    
        print("""
Action:\t[Lists] computer
Tool:\tbloodyAD
Option:\t-u, --username
\t-p --password; -H, --hash; -k
Desc:\tLists all computers and saves them in the file computer.lst
Info:\t/
        """)
        return 0
    config.required_creds(box)
    os.chdir(path.ws_lst)
    print('\033[92m[*]\033[0m List Domain Computers')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} bloodyAD --host {box.fqdn} -d {box.domain} -k get children --otype computer"
    elif box.krb:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} -k get children --otype computer"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} get children --otype computer"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} get children --otype computer"
    cmd = cmd+ """ | awk -F'CN=' '{split($2,a,","); print a[1]}' | sed '/^$/d' | sed 's/$/$/'"""
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+ ' 2>&1 | tee computer.lst')
    print('\033[38;5;28m[+]\033[0m List Domain Computers\n')

def groups(box, path):
    if config.HELP:    
        print("""
Action:\t[Lists] group
Tool:\tbloodyAD
Option:\t-u, --username
\t-p --password; -H, --hash; -k
Desc:\tLists all groups and saves them in the file group.lst
Info:\t/
        """)
        return 0
    config.required_creds(box)
    os.chdir(path.ws_lst)
    print('\033[92m[*]\033[0m List Domain Groups')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} bloodyAD --host {box.fqdn} -d {box.domain} -k get children --otype group"
    if box.krb:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} -k get children --otype group"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} get children --otype group"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} get children --otype group"
    cmd = cmd+ """ | awk -F'CN=' '{split($2,a,","); print a[1]}' | sed '/^$/d'"""
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+ ' 2>&1 | tee group.lst')
    print('\033[38;5;28m[+]\033[0m List Domain Groups\n')