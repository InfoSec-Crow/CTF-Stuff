import os 
import config

def smb_view(box, path):
    config.required_creds(box)
    os.chdir(path.ws_enum)
    print('\033[93m[*]\033[0m List SMB shares & files')
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} netexec smb {box.fqdn} --use-kcache --shares"
        cmd2 = f"{box.krb_ccache} netexec smb {box.fqdn} --use-kcache -M spider_plus"
        cmd3 = f"{box.krb_ccache} impacket-smbclient -k -no-pass {box.fqdn}"
    elif box.krb:
        cmd = f"netexec smb {box.fqdn} -u {box.username} -p {box.password} -k --shares"
        cmd2 = f"netexec smb {box.fqdn} -u {box.username} -p {box.password} -k -M spider_plus"
        cmd3 = f"impacket-smbclient -k {box.domain}/{box.username}:{box.password}@{box.fqdn}"
    elif box.nt_hash:
        cmd = f"netexec smb {box.fqdn} -u {box.username} -H {box.nt_hash} --shares"
        cmd2 = f"netexec smb {box.fqdn} -u {box.username} -H {box.nt_hash} -M spider_plus"
        cmd3 = f"impacket-smbclient {box.domain}/{box.username}@{box.fqdn} -hashes :{box.nt_hash}"
    else:
        cmd = f"netexec smb {box.fqdn} -u {box.username} -p {box.password} --shares"
        cmd2 = f"netexec smb {box.fqdn} -u {box.username} -p {box.password} -M spider_plus"
        cmd3 = f"impacket-smbclient {box.domain}/{box.username}:{box.password}@{box.fqdn}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    filter = " | awk '/Share/ {f=1} f' | sed 's/^SMB.*"+box.hostname+"[[:space:]]\\+//'"
    os.system(cmd+filter+f' | tee {box.username}_smb-shares.txt')
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    out = os.popen(cmd2).read()
    print('\n'.join(out.splitlines()[-10:]))
    os.system(f'cp /home/kali/.nxc/modules/nxc_spider_plus/{box.fqdn}.json .')
    print(f'[*] Output file: /home/kali/.nxc/modules/nxc_spider_plus/{box.fqdn}.json')
    print(f'\n\033[96m[$]\033[0m {cmd3}')
    print('\033[92m[+]\033[0m List SMB shares\n')

def winrm(box, path, cmd):
    config.required_creds(box)
    #os.chdir(path.ws_scr)
    print('\033[93m[*]\033[0m Login to WinRm (run CMD)')
    ps_cmd = ""
    if cmd:
        if cmd.replace(".txt","") == "user":
            ps_cmd = f'''echo "gc (join-path ([Environment]::GetFolderPath('Desktop')) user.txt)" | '''
        elif cmd.replace(".txt","") == "root":
            ps_cmd = f'''echo "type /Users/Administrator/Desktop/root.txt" | '''
        else:
            ps_cmd = f'''echo "{cmd}" | '''
    if box.krb or isinstance(box.krb, str):
        cmd = f"{ps_cmd}{box.krb_ccache} evil-winrm -i {box.fqdn} -r {box.domain}"
    elif box.nt_hash:
        cmd = f"{ps_cmd}evil-winrm -i {box.fqdn} -u {box.username} -H {box.nt_hash}"
    else:
        cmd = f"{ps_cmd}evil-winrm -i {box.fqdn} -u {box.username} -p {box.password}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m Login to WinRm')

def ldap(box, path, cmd):
    config.required_creds(box)
    os.chdir(path.ws_enum)
    print('\033[93m[*]\033[0m Login to LDAP (run Query)')
    ps_cmd = ""
    if cmd:
        if cmd == "?":
            pass
        else:
            query = f"--query '{cmd}' ''"
    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} netexec ldap {box.fqdn} --use-kcache {query}"
    elif box.krb:
        cmd = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} -k {query}"
    elif box.nt_hash:
        cmd = f"netexec ldap {box.fqdn} -u {box.username} -H {box.nt_hash} {query}"
    else:
        cmd = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} {query}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    print('\033[92m[+]\033[0m Login to LDAP')
