#!/usr/bin/python3
import argparse
import os

parser = argparse.ArgumentParser(
    description="Rustscan and Nmap for CTFs",
    formatter_class=argparse.RawTextHelpFormatter,
)
parser.add_argument("-i", "--ip", required=True, type=str)
parser.add_argument("-n", "--name", type=str, help="Name for the output file")
args = parser.parse_args()

if args.name:
    name = args.name
else:
    name = os.path.basename(os.getcwd())

filename = f"{name}_nmap-scan.txt"
cmd = f"rustscan -a {args.ip} -- -sC -sV -oN {filename}"
print(f"\n[$] {cmd}")
os.system(cmd)
print(f"\n[+] Save outout in file: {filename}")