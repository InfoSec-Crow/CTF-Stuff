import os
import config

def add_user_to_group(box):
    print(f'\033[93m[*]\033[0m Add user to group')
    print(f'\033[95m[>]\033[0m Target: {box.target} --> {box.targetgroup}')
    cmd = f"impacket-net {box.domain}/{box.username}:'{box.password}'@{box.fqdn} group -name '{box.targetgroup}' -join {box.target}"
    config.log_cmd(cmd)
    os.system(cmd+config.VERBOSE[0])
    print('\033[92m[+]\033[0m Add user to group')

def list_user_to_group(box):
    print(f'\033[93m[*]\033[0m List users in group')
    print(f'\033[95m[>]\033[0m Target: {box.targetgroup}')
    cmd = f"impacket-net {box.domain}/{box.username}:'{box.password}'@{box.fqdn} group -name '{box.targetgroup}'"
    config.log_cmd(cmd)
    os.system(cmd+config.VERBOSE[0])
    print('\033[92m[+]\033[0m List users in group')

def remove_user_to_group(box):
    print(f'\033[93m[*]\033[0m Remove user from group')
    print(f'\033[95m[>]\033[0m Target: {box.target} -x-> {box.targetgroup}')
    cmd = f"impacket-net {box.domain}/{box.username}:'{box.password}'@{box.fqdn} group -name '{box.targetgroup}' -unjoin {box.target}"
    config.log_cmd(cmd)
    os.system(cmd+config.VERBOSE[0])
    print('\033[92m[+]\033[0m Remove user from group')