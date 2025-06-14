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

