import os
from datetime import datetime, timedelta
import pytz
import re
import subprocess
import settings

HELP = False
SKIP = False
QUITE = False
CWD = None
OUTPUT_FILE = None

def get_tun0_ip():
    try:
        ip = subprocess.check_output("ip a | grep -A 2 'tun0:' | grep -oP '(?<=inet\\s)\\d+(\\.\\d+){3}'", shell=True).decode().strip()
    except:
        print('\033[93m[-]\033[0m No tun0, use 127.0.0.1')
        ip = '127.0.0.1'
    return ip

def show_menu(title, menu):
    print(f"[--- {title} Menu ---]")
    for index, text in enumerate(menu, start=1):
        print(f"{index}. {text}")
    try:
        choice = input("\n\033[94m[>]\033[0m Choose nummber: ").strip()
        if not choice.isdigit() or int(choice) > len(menu) or int(choice) == 0:
           print("\033[93m[-]\033[0m Wrong Input")
           show_menu(title, menu)
        return int(choice)
    except KeyboardInterrupt:
        exit()

def ask_for_action_choice(options):
    default = options.split(",")[0].lower()
    try:
        if not SKIP:
            user_input = input(f"\033[94m[>]\033[0m Choose one [{options}]: ").strip().lower() or default
        else:
            print(f"\033[94m[>]\033[0m Choose one [{options}]: {default}")
            user_input = default
        return user_input
    except KeyboardInterrupt:
        exit(0)

def ip_in_hosts(ip):
    found = False
    with open(settings.HOSTS_FILE, "r") as f:
        for line in f:
            if ip in line:
                found = True
                break
    if found:
        return True
    else:
        return False

def clear_hosts_entry():
    print(f"[*] Clear {settings.HOSTS_FILE} entries (*.htb)")
    with open(settings.HOSTS_FILE) as f:
        lines = [line for line in f if ".htb" not in line]
    with open(settings.HOSTS_FILE, "w") as f:
        f.writelines(lines)

def get_hosts_entry():
    with open(settings.HOSTS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_line = lines[-1].strip() if lines else ""
    l = [x for x in last_line.split() if x]
    return l

class PATH:
    @classmethod
    def setup(cls, name=None):
        if not name:
            cls.ws = None
            cls.ws_log = None
            cls.ws_enum = None
            cls.ws_lst = None
            cls.ws_atk = None
            cls.ws_ccache = None
            cls.ws_adcs = None
            cls.ws_scr = None
            return

        cls.ws = f'{settings.WS_PATH}{name}/adkit'
        cls.ws_log = f'{cls.ws}/log/'
        cls.ws_enum = f'{cls.ws}/enum/'
        cls.ws_lst = f'{cls.ws}/lst/'
        cls.ws_atk = f'{cls.ws}/atk/'
        cls.ws_ccache = f'{cls.ws}/ccache/'
        cls.ws_adcs = f'{cls.ws}/adcs/'
        cls.ws_scr = f'{cls.ws}/scr/'


def de_timestemp():
    utc_now = datetime.now(pytz.utc)
    de_time = utc_now - timedelta(hours=2)
    return de_time.strftime("[%Y-%m-%d %H:%M:%S]")

def log_cmd(content):
    path = PATH()
    if path.ws_log:
        log_path = f'{path.ws_log}/{settings.CMD_LOG_FILE}'
    else: 
        log_path = f"/tmp/{settings.CMD_LOG_FILE}"
    if content:
        if isinstance(content, list):
            content = [line.strip() for line in content if line.strip()]
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
            else:
                lines = []
            new_line = [line for line in content if line not in lines]
            if new_line:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(de_timestemp() + '\n')
                    for line in new_line:
                        f.write(line + '\n')
        else:
            line = content.strip()
            if os.path.exists(log_path):
                with open(log_path, "r", encoding="utf-8") as f:
                    lines = f.read().splitlines()
            else:
                lines = []
            if line not in lines:
                with open(log_path, "a", encoding="utf-8") as f:
                    f.write(de_timestemp() + '\n')
                    f.write(line + '\n')

def set_hosts_entry(ip):
    clear_hosts_entry()
    user_input = ask_for_action_choice("NMAP,nxc")
    if user_input.lower() == "nmap":
        print('\033[95m[*]\033[0m Generate hosts file (nmap)')
        cmd = f'nmap {ip} -p 389 --script ldap-rootdse'
        print(f'\033[96m[$]\033[0m {cmd}')
        output = os.popen(cmd).read()
        try:
            match = re.search(r'dnsHostName:\s*(\S+)', output)
            fqdn = match.group(1)
            e = fqdn.split(".")
        except AttributeError:
            print("\033[93m[-]\033[0m ERROR: Output missing dnsHostName entry. Try again!")
            exit()
        os.system(f'echo "{ip} {fqdn} {e[1]}.{e[2]} {e[0]}" | tee -a {settings.HOSTS_FILE}')
        print('\033[38;5;28m[+]\033[0m Generate hosts file\n')
    elif user_input.lower() == "nxc":
        print('\033[92m[*]\033[0m Generate hosts file (nxc)')
        cmd = f'netexec smb {ip} --generate-hosts-file {settings.HOSTS_FILE}'
        print(f'\033[96m[$]\033[0m {cmd}')
        os.system(cmd)
        os.system(f'tail -n1 {settings.HOSTS_FILE}')
        print('\033[38;5;28m[+]\033[0m Generate hosts file\n')
    else:
        print("\033[91m[!]\033[0m Incorrect input!")
        exit()

def nt_hashing(password):
    if password:
        cmd = f"pypykatz crypto nt {password}"
        return os.popen(cmd).read().strip()
    else:
        print('''\033[91m[!]\033[0m Required a hash or password for -H, --hash!
        ''')
        exit()

def required_creds(box):
    if box.krb_ccache:
        return
    if box.username and (box.password or box.nt_hash):
        return
    print('''\033[91m[!]\033[0m Required!
    -u, --username 
    -p, --password or -H, --hash
            ''')
    exit()
        
def required_target(box):
    if not box.target:
        print('''\033[91m[!]\033[0m Required!
    -t, --target
        ''')
        exit()

def required_targetgroup(box):
    if not box.targetgroup:
        print('''\033[91m[!]\033[0m Required!
    -tg, --targetgroup
        ''')
        exit()

def required_ca(box):
    if not box.ca:
        print('''\033[91m[!]\033[0m Required!
    -ca
        ''')
        exit()

def time_sync(fqdn):
    os.system(f'sudo ntpdate {fqdn} > /dev/null 2>&1')

def check_krb_config(domain):
    with open(settings.KRB_FILE) as f:
        if domain not in f.read():
            print(f"\033[93m[-]\033[0m Your {settings.KRB_FILE} file has not been generated yet, use -a krb")
            try:
                input("    Continue? [ENTER]")
            except KeyboardInterrupt:
                exit(0)

def kerberos_auth(box, path, username_=None, password_=None):
    required_creds(box)
    os.chdir(path.ws_ccache)
    username = box.username
    password = box.password
    if username_ and password_:
        username = username_
        password = password_
    if not os.path.exists(f'{box.username}.ccache'):
        print('\033[92m[*]\033[0m Get TGT')
        time_sync(box.fqdn)
        if box.nt_hash and (not username_ and not password_):
            cmd = f"impacket-getTGT {box.domain}/{username} -hashes :{box.nt_hash}"
        else:
            cmd = f"impacket-getTGT {box.domain}/{username}:{password}"
        log_cmd(cmd)
        print(f'\033[96m[$]\033[0m {cmd}')
        os.system(cmd)
        print('\033[38;5;28m[+]\033[0m Get TGT\n')
    return f"{path.ws_ccache}{box.username}.ccache"