#!/usr/bin/python3
import argparse
import subprocess, os
from pathlib import Path
from pl.php_pl import php_pl
from pl.bash_pl import bash_pl
from pl.ps_pl import ps_pl 

def get_tun0_ip():
    try:
        ip = subprocess.check_output("ip a | grep -A 2 'tun0:' | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'", shell=True).decode().strip()
    except:
        print('No tun0 - use 127.0.0.1')
        ip = '127.0.0.1'
    return ip

parser = argparse.ArgumentParser(description='Payload maker')
parser.add_argument("--lhost", type=str, default=get_tun0_ip(), help='local host (default: tun0)')
parser.add_argument("--lport", type=int, default=1234, help='local port (default: 1234)')
args = parser.parse_args()

original_script_path = Path(__file__).resolve()
PL_PATH = str(original_script_path.parent) + '/payloads/'

def main():
    print("=== Make Payload ===")
    print("\n1. PHP\n2. Bash \n3. Powershell")
    choice = input(": ")
    if choice == "1":
        php_pl(args, PL_PATH).menu()
    elif choice == "2":
        bash_pl(args, PL_PATH).menu()
    elif choice == "3":
        ps_pl(args, PL_PATH).menu()
    exit()

if __name__ == "__main__":
    main()
