import os
from datetime import datetime, timedelta
import pytz

WS_PATH = '/home/kali/htb/box/'
CMD_LOG_FILE = 'commands.log'
VERBOSE = None

def get_hosts_entry():
    with open("/etc/hosts", "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_line = lines[-1].strip() if lines else ""
    l = [x for x in last_line.split() if x]
    return l

class Box:
    try:
        l = get_hosts_entry()
        ip = l[0]
        fqdn = l[1].lower()
        hostname = l[3].lower()
        domain = l[2].lower()
        name = l[1].split('.')[1].lower()
        username = None
        password = None
        nt_hash = None
        krb = None
        target = None
        targetgroup = None
    except:
        print(f'\033[91m[!]\033[0m Host entry not there or wrong!\n\tFormat: IP FQDN DOMAIN HOSTNEM')

class PATH:
    ws = None
    ws_log = None
    ws_dump = None
    ws_lst = None
    ws_atk = None
    ws_adcs = None

    @classmethod
    def setup(cls, name):
        cls.ws = f'{WS_PATH}{name}'
        cls.ws_log = f'{cls.ws}/log/'
        cls.ws_enum = f'{cls.ws}/enum/'
        cls.ws_lst = f'{cls.ws}/lst/'
        cls.ws_atk = f'{cls.ws}/atk/'
        cls.ws_ccache = f'{cls.ws}/ccache/'
        cls.ws_adcs = f'{cls.ws}/adcs/'

def de_timestemp():
    utc_now = datetime.now(pytz.utc)
    de_time = utc_now - timedelta(hours=2)
    return de_time.strftime("[%Y-%m-%d %H:%M:%S]")

def log_cmd(content):
    path = PATH()
    log_path = f'{path.ws_log}/{CMD_LOG_FILE}'
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
    print('\033[93m[*]\033[0m Generate hosts file')
    cmd = f'netexec smb {ip} --generate-hosts-file /etc/hosts'
    print(f'\033[96m[$]\033[0m {cmd}')
    os.system(cmd)
    os.system('tail -n1 /etc/hosts')
    print('\033[92m[+]\033[0m Generate hosts file\n')

def nt_hashing(box, nt_hash):
    if nt_hash == 'empty':
        if box.password:
            cmd = f"pypykatz crypto nt '{box.password}'"
            return os.popen(cmd).read().strip()
        else:
            print('''\033[91m[!]\033[0m Required a hash or password for -H, --hash!
            ''')
            exit()
    else:
        return nt_hash.strip()

def required_creds(box):
    if box.password or box.nt_hash or box.krb or os.path.exists(f'{box.username}.ccache'):
        if box.username:
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

def kerberos_auth(box, path):
    required_creds(box)
    os.chdir(path.ws_ccache)
    if not os.path.exists(f'{box.username}.ccache'):
        print('\033[93m[*]\033[0m Get TGT')
        os.system(f'sudo ntpdate {box.fqdn} > /dev/null 2>&1')
        if box.nt_hash:
            cmd = f"impacket-getTGT {box.domain}/{box.username} -hashes :{box.nt_hash}"
        else:
            cmd = f"impacket-getTGT {box.domain}/{box.username}:'{box.password}'"
        log_cmd(cmd)
        print(f'\033[96m[$]\033[0m {cmd}')
        os.system(cmd)
        print('\033[92m[+]\033[0m Get TGT\n')
    return f"KRB5CCNAME='{path.ws_ccache}{box.username}.ccache'"
