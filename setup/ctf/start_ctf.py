#!/usr/bin/python3

import os
import argparse
import subprocess

WS_PATH = '/home/kali/Desktop/htb/box/'

parser = argparse.ArgumentParser(description='CTF start commands')
parser.add_argument("-n","--name", required=True, type=str, help='Name')
parser.add_argument("-i", "--ip", required=True, type=str, help='IP')
parser.add_argument('-w', '--windows', action='store_true', help='Adds windows domain to /etc/hosts')
args = parser.parse_args()

if args.windows:
    os.system(f'netexec smb {args.ip} --generate-hosts-file /etc/hosts')

def folder():
    os.makedirs(f'{WS_PATH}{args.name}', exist_ok=True)
    print(f'Make folder: {WS_PATH}{args.name}')

def hosts():
    entry = f"{args.ip}\t{args.name.lower()}.htb"
    with open('/etc/hosts', "a") as file:
        file.write(f"\n{entry}\n")

def nmap():
    nmap_command = f"nmap -v -sC -sV -oN {args.name}.nmap {args.ip}"
    process = subprocess.Popen(nmap_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    for stdout_line in iter(process.stdout.readline, ""):
        print(stdout_line, end="")
    for stderr_line in iter(process.stderr.readline, ""):
        print(stderr_line, end="")
    process.stdout.close()
    process.stderr.close()
    process.wait()

folder()
hosts()
os.chdir(f'{WS_PATH}{args.name}')
os.system(f'echo "cd {WS_PATH}{args.name}" | xclip -selection clipboard')
nmap()
