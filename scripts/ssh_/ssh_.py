#!/usr/bin/python3

import argparse
import os
import subprocess

def current_folder():
    return os.path.basename(os.getcwd()).lower()

parser = argparse.ArgumentParser(description='SSH login with sshpass')
parser.add_argument("-i", "--host", type=str, default=f'{current_folder()}.htb', help='Target hostname (default: <current foldername>.htb)')
parser.add_argument("-u", "--username", required=True, type=str)
parser.add_argument("-p", "--password", required=True, type=str)
parser.add_argument("-up", type=str, help='Filepath for the upload')
parser.add_argument("-down", type=str, help='Filepath for the download')
parser.add_argument("-auto", type=str, nargs='?', default=None, const='/opt/CTF-Stuff/scripts/ssh_/auto.txt', help='Listfile that contains fileapaths for automatic uploading (default: /opt/CTF-Stuff/scripts/ssh_/auto.txt)')
parser.add_argument("-path", type=str, help='Path to to upload destination (default: upload=/dev/shm/, dowload=pwd)')
parser.add_argument("-x", "--cmd", type=str, help='Run single command')
args = parser.parse_args()

def upload_file(up, path):
    if not args.path:
        path = '/dev/shm/'
    print(f'[*] Upload file: {up} to {path}\n')
    cmd = f"sshpass -p '{args.password}' rsync -av --progress -e 'ssh -o StrictHostKeyChecking=no' '{up}' {args.username}@{args.host}:'{path}'"
    subprocess.run(cmd, shell=True, check=True)
    print('\n[+] Done!')

# Uplaod File
if args.up:
    try:
        upload_file(args.up, args.path)
    except:
        print(f'\n[-] Upload failed!')
    exit()

# Download File
if args.down:
    if not args.path:
        args.path = './'
    try:
        print(f'[*] Download file: {args.down} to {args.path}\n')
        cmd = f"sshpass -p '{args.password}' rsync -av --progress -e 'ssh -o StrictHostKeyChecking=no' {args.username}@{args.host}:'{args.down}' '{args.path}'"
        subprocess.run(cmd, shell=True, check=True)
        print('\n[+] Done!')
    except:
        print(f'\n[-] Download failed!')
    exit()

# Automatic uploading
if args.auto:
    print(f'[*] Automatic uploading files from: {args.auto}')
    try:
        with open(args.auto, 'r') as file:
            for line in file:
                filepath = line.strip()
                upload_file(filepath, args.path)
    except Exception as e:
        print(f'\n[-] Auto Error: {e}')
    exit()

cmd = f"sshpass -p '{args.password}' ssh {args.username}@{args.host} -o StrictHostKeychecking=no"
if args.cmd:
    cmd = cmd + f' {args.cmd}'
print(f'[*] Run: {cmd}')
os.system(cmd)
