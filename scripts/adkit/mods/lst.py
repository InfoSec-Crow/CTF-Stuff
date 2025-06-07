import os
import config

def users(box, path):
    print('\033[93m[*]\033[0m List Domain Users')
    os.chdir(path.ws_lst)
    cmd = f"bloodyAD -u {box.username} -p '{box.password}' -d {box.domain} --host {box.ip} get children --otype user"
    filter = """ | awk -F'CN=' '{split($2,a,","); print a[1]}' | sed '/^$/d'"""
    config.log_cmd(cmd+filter)
    if config.VERBOSE == ['']:
        os.system(cmd + filter + ' 2>&1 | tee user.lst')
    else:
        os.system(cmd + filter + ' > user.lst 2>&1')
    print('\033[92m[+]\033[0m List Domain Users')

def computers(box, path):
    print('\033[93m[*]\033[0m List Domain Computers')
    os.chdir(path.ws_lst)
    cmd = f"bloodyAD -u {box.username} -p '{box.password}' -d {box.domain} --host {box.ip} get children --otype computer"
    filter = """ | awk -F'CN=' '{split($2,a,","); print a[1]}' | sed '/^$/d' | sed 's/$/$/'"""
    config.log_cmd(cmd+filter)
    if config.VERBOSE == ['']:
        os.system(cmd + filter + ' 2>&1 | tee computer.lst')
    else:
        os.system(cmd + filter + ' > computer.lst 2>&1')
    print('\033[92m[+]\033[0m List Domain Computers')

def groups(box, path):
    print('\033[93m[*]\033[0m List Domain Groups')
    os.chdir(path.ws_lst)
    cmd = f"bloodyAD -u {box.username} -p '{box.password}' -d {box.domain} --host {box.ip} get children --otype group"
    filter = """ | awk -F'CN=' '{split($2,a,","); print a[1]}' | sed '/^$/d'"""
    config.log_cmd(cmd+filter)
    if config.VERBOSE == ['']:
        os.system(cmd + filter + ' 2>&1 | tee group.lst')
    else:
        os.system(cmd + filter + ' > group.lst 2>&1')
    print('\033[92m[+]\033[0m List Domain Groups')