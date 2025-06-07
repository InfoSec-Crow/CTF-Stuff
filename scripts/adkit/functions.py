import os
import sys

def get_hosts_entry():
    with open("/etc/hosts", "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_line = lines[-1].strip() if lines else ""
    l = [x for x in last_line.split() if x]
    return l

def log_cmd(content, ws_log, file_log):
    if content:
        line = content.strip()
        log_path = f'{ws_log}/{file_log}'
        if os.path.exists(log_path):
            with open(log_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
        else:
            lines = []
        if line not in lines:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + '\n')