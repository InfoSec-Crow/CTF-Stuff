def generate_hosts():
    with open('/etc/hosts', "r", encoding="utf-8") as f:
        content = f.read()
    if re.search(rf'\b{re.escape(IP)}\b', content):
        print('[+] Generate hosts file - entry already exists')
    else:
        if args.os == 'l':
            entry = f"{IP}\t{NAME.lower()}.htb"
            with open('/etc/hosts', "a") as file:
                file.write(f"\n{entry}\n")
            print('[+] Generate hosts file')
            return None
        elif args.os == 'w':
            cmd = f'netexec smb {IP} --generate-hosts-file /etc/hosts'
            os.system(cmd+VERBOSE[0])
            print('[+] Generate hosts file')
            return cmd


def nmap_scan():
    if os.path.exists(f'{WS_PATH}/{NAME}.nmap'):
        print(f"[!] Nmap output file exists! {WS_PATH}/{NAME}/{NAME}.nmap")
    else:
        print('[*] Start Nmap scan...')
        cmd = f"nmap -v -sC -sV -oN {WS_PATH}/{NAME}/{NAME}.nmap {IP}"
        log_cmd(cmd)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if args.VERBOSE:
            for stdout_line in iter(process.stdout.readline, ""):
                print(stdout_line, end="")
            for stderr_line in iter(process.stderr.readline, ""):
                print(stderr_line, end="")
        else:
            process.stdout.read()
            process.stderr.read()
        process.stdout.close()
        process.stderr.close()
        process.wait()
        print('[+] Nmap scan finished')