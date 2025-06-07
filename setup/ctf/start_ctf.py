#!/usr/bin/python3

import os
import argparse
import subprocess

parser = argparse.ArgumentParser(description='CTF setup')
parser.add_argument("-i", "--ip", required=True, type=str, help='')
parser.add_argument("-n","--name", type=str.lower, help='Name of the Box')
parser.add_argument('-x', '--nonmap', action='store_true', help='No Nmap scan')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-w', '--windows', action='store_true', help='Windows Target')
group.add_argument('-l', '--linux', action='store_true', help='Linux Target')
args = parser.parse_args()

def make_folder(path):
    os.makedirs(path, exist_ok=True)
    print(f'[+] Folder: {path}')

def get_hosts_last_entry():
    with open("/etc/hosts", "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_line = lines[-1].strip() if lines else ""
            print(f'[+] Entry: {last_line}')
    return [x for x in last_line.split() if x]

def nmap(name):
    print('[+] Nmap Scan')
    nmap_command = f"nmap -v -sC -sV -oN {name}.nmap {args.ip}"
    process = subprocess.Popen(nmap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for stdout_line in iter(process.stdout.readline, ""):
        print(stdout_line, end="")
    for stderr_line in iter(process.stderr.readline, ""):
        print(stderr_line, end="")
    process.stdout.close()
    process.stderr.close()
    process.wait()

if args.linux:
    if not args.name:
        print('[!] Missing -n argument for Box name!')
        exit()
    print('[*] Start setup for Linux target...')
    name = args.name
    path = f'/home/kali/Desktop/htb/box/{name}'
    make_folder(path)
    entry = f"{args.ip}\t{name}.htb"
    with open('/etc/hosts', "a") as file:
        file.write(f"\n{entry}\n")
    get_hosts_last_entry()

elif args.windows:
    print('[*] Start setup for Windows target...')
    os.system(f'netexec smb {args.ip} --generate-hosts-file /etc/hosts > /dev/null 2>&1')
    l = get_hosts_last_entry()
    name = l[1].split('.')[1]
    path = f'/home/kali/Desktop/htb/box/{name}'
    make_folder(path)

os.chdir(path)
if not args.nonmap:
    nmap(name)
print('[*] Setup completed!')