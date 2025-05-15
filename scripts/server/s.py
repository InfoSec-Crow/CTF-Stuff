#!/usr/bin/python3
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Simple HTTP Server for PHP, Python')
parser.add_argument('-t', '--type', type=str, default='py', help='Server Type (default: python)')
parser.add_argument('-lh', '--lhost', type=str, default='0.0.0.0', help='local ip (default:0.0.0.0)')
parser.add_argument('-lp', '--lport', type=str, default='80', help='local port (default:80)')
args = parser.parse_args()

def run_cmd(cmd):
    try:
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True) as proc:
            print(cmd)
            print(f'[*] Running on {args.lhost}:{args.lport}\n')
            for line in proc.stdout:
                print(line, end='')
    except KeyboardInterrupt:
        print("\n[!] Exit.")
    except Exception as e:
        print(f"[!] Error: {e}")

if args.type.lower() == 'php':
    run_cmd(f'sudo php -S {args.lhost}:{args.lport}')

elif args.type.lower() == 'py' or args.type.lower() == 'python':
    run_cmd(f'sudo python3 -m http.server {args.lport} --bind {args.lhost}')