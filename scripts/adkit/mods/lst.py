import os
import config

def users(box, path):
    os.chdir(path.ws_lst)
    print('\033[93m[*]\033[0m List Domain Users')
    cmd = f"bloodyAD -u {box.username} -p '{box.password}' -d {box.domain} --host {box.ip} get children --otype user"
    cmd = cmd+ """ | awk -F'CN=' '{split($2,a,","); print a[1]}' | sed '/^$/d'"""
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+ ' 2>&1 | tee user.lst')
    print('\033[92m[+]\033[0m List Domain Users')

def computers(box, path):
    os.chdir(path.ws_lst)
    print('\033[93m[*]\033[0m List Domain Computers')
    cmd = f"bloodyAD -u {box.username} -p '{box.password}' -d {box.domain} --host {box.ip} get children --otype computer"
    cmd = cmd+ """ | awk -F'CN=' '{split($2,a,","); print a[1]}' | sed '/^$/d' | sed 's/$/$/'"""
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+ ' 2>&1 | tee computer.lst')
    print('\033[92m[+]\033[0m List Domain Computers')

def groups(box, path):
    os.chdir(path.ws_lst)
    print('\033[93m[*]\033[0m List Domain Groups')
    cmd = f"bloodyAD -u {box.username} -p '{box.password}' -d {box.domain} --host {box.ip} get children --otype group"
    cmd = cmd+ """ | awk -F'CN=' '{split($2,a,","); print a[1]}' | sed '/^$/d'"""
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd+ ' 2>&1 | tee group.lst')
    print('\033[92m[+]\033[0m List Domain Groups')