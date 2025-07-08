#!/usr/bin/python3
import os
import argparse

parser = argparse.ArgumentParser(
    description="Time Sync",
    formatter_class=argparse.RawTextHelpFormatter
)
parser.add_argument("-i", "--fqdn", type=str, help="FQDN to sync")
args = parser.parse_args()

def get_hosts_entry():
    with open("/etc/hosts", "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_line = lines[-1].strip() if lines else ""
    l = [x for x in last_line.split() if x]
    return l
if args.fqdn:
    fqdn = args.fqdn
else:
    l = get_hosts_entry()
    fqdn = l[1]
cmd = f"sudo ntpdate {fqdn}"
print(f'\033[96m[$]\033[0m {cmd}')
os.system(cmd)