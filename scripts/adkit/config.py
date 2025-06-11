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
        cls.ws = f'{WS_PATH}{name}'
        cls.ws_log = f'{cls.ws}/log'
        cls.ws_enum = f'{cls.ws}/enum'
        cls.ws_lst = f'{cls.ws}/lst'
        cls.ws_atk = f'{cls.ws}/atk'

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
