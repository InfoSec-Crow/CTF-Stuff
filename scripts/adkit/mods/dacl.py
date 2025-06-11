import os
import config

def add_user_to_group(box):
    """
    target required
    tagetgroup required
    """
    print(f'\033[93m[*]\033[0m Add user to group')
    #cmd = f"impacket-net {box.domain}/{box.username}:'{box.password}'@{box.fqdn} group -name '{box.targetgroup}' -join {box.target}"
    cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p '{box.password}' add groupMember {box.targetgroup} {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m Add user to group')

def list_user_to_group(box):
    """
    tagetgroup required
    """
    print(f'\033[93m[*]\033[0m List users in group')
    cmd = f"impacket-net {box.domain}/{box.username}:'{box.password}'@{box.fqdn} group -name '{box.targetgroup}'"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m List users in group')

def remove_user_to_group(box):
    """
    target required
    tagetgroup required
    """
    print(f'\033[93m[*]\033[0m Remove user from group')
    #cmd = f"impacket-net {box.domain}/{box.username}:'{box.password}'@{box.fqdn} group -name '{box.targetgroup}' -unjoin {box.target}"
    cmd = f"bloodyAD --host {box.fqdn} -d {box.domain} -u {box.username} -p '{box.password}' remove groupMember {box.targetgroup} {box.target}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m Remove user from group')