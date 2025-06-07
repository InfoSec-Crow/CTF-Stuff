import os

CMD_LOG_FILE = 'commands.log'
VERBOSE = None

def get_hosts_entry():
    with open("/etc/hosts", "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_line = lines[-1].strip() if lines else ""
    l = [x for x in last_line.split() if x]
    return l

class Box:
    l = get_hosts_entry()
    ip = l[0]
    fqdn = l[1].lower()
    hostname = l[3].lower()
    domain = l[2].lower()
    name = l[1].split('.')[1].lower()
    username = None
    password = None
    target = None
    targetgroup = None

class PATH:
    ws = None
    ws_log = None
    ws_dump = None
    ws_lst = None
    ws_atk = None

    @classmethod
    def setup(cls, name):
        cls.ws = f'/home/kali/Desktop/htb/box/{name}'
        cls.ws_log = f'{cls.ws}/log'
        cls.ws_enum = f'{cls.ws}/enum'
        cls.ws_lst = f'{cls.ws}/lst'
        cls.ws_atk = f'{cls.ws}/atk'

def log_cmd(content):
    if content:
        line = content.strip()
        path = PATH()
        log_path = f'{path.ws_log}/{CMD_LOG_FILE}'
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        else:
            lines = []
        if line not in lines:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + '\n')