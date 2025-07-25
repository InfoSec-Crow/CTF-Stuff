import config

class Box:
    def __init__(self):
        self.username = None
        self.password = None
        self.nt_hash = None
        self.krb = None
        self.krb_ccache = None
        self.target = None
        self.targetgroup = None
        self.ca = None
        self.file = None
        try:
            l = config.get_hosts_entry()
            self.ip = l[0]
            self.fqdn = l[1].lower()
            self.hostname = l[3].lower()
            self.domain = l[2].lower()
            self.name = l[1].split('.')[1].lower()
        except:
            self.ip = None
            self.fqdn = None
            self.hostname = None
            self.domain = None
            self.name = None
            print(f'\033[91m[!]\033[0m Host entry not there or wrong!\n\tFormat: \033[93m IP FQDN DOMAIN HOSTNEM \033[0m')

def info(box):
    if not config.QUITE and box.ip:
        info = {
        "NAME": box.name,
        "IP": box.ip,
        "HOSTNAME": box.hostname,
        "FQDN": box.fqdn,
        "DOMAIN": box.domain,
        }
        if box.username and box.target:
            info['USERNAME'] = box.username
        elif box.username and not box.target:
            info['USERNAME/TARGET'] = box.username
        if box.password:
            info['PASSWORD'] = box.password
        if box.nt_hash:
            info['HASH'] = box.nt_hash
        if box.krb:
            info['CCACHE'] = box.krb
        if box.target:
            info['TARGET'] = box.target
        if box.targetgroup:
            info['TARGETGROUP'] = box.targetgroup
        if box.file:
            info['FILE'] = box.file
        key_width = 17
        val_width = 35
        line = f"\033[96m+\033[0m{'-'*key_width}\033[96m•\033[0m{'-'*val_width}\033[96m+\033[0m"
        print(line)
        for i, (key, val) in enumerate(info.items(), start=1):
            print(f"| {key:<{key_width-1}}\033[96m:\033[0m {val:<{val_width-1}}|")
            if i % 5 == 0:
                print(line)
        if len(info.items()) > 5:
            print(line)
    print()