#!/usr/bin/python3

import argparse
import os

def current_folder():
    return os.path.basename(os.getcwd()).lower()

parser = argparse.ArgumentParser(description='SSH login with sshpass')
parser.add_argument("-i", "--host", type=str, default=f'{current_folder()}.htb', help='Hostname (default: <current foldername>.htb')
parser.add_argument("-u", "--username", required=True, type=str)
parser.add_argument("-p", "--password", required=True, type=str)
args = parser.parse_args()

cmd = f"sshpass -p '{args.password}' ssh {args.username}@{args.host} -o StrictHostKeychecking=no"
print(cmd)
print()
os.system(cmd)
