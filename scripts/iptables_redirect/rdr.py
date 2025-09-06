#!/usr/bin/python3
import os
import re

B = "\033[94m"
G = "\033[92m"
R = "\033[91m"  
X = "\033[0m"
IPTABLES = {}

def overview():
    global IPTABLES
    cmd_out = os.popen("sudo iptables -t nat -S | grep REDIRECT").read()
    matches = re.findall(r"--dport (\d+).*--to-ports (\d+)", cmd_out)
    ports = [(int(src), int(dst)) for src, dst in matches]
    print("≡≡≡≡ PREROUTING ≡≡≡≡")
    for src, dst in ports:
        print(f"{src}\t{B}➤➤➤{X}\t{dst}")
        IPTABLES[src] = dst
    print("≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡≡")

def add(src,dst):
    try:
        cmd = f"iptables -t nat -A PREROUTING -p tcp --dport {src} -j REDIRECT --to-port {dst}"
        os.system(cmd)
        print(f"{src}\t{G}➤➤➤{X}\t{dst}")
    except Exception as e:
        print(f"An error occurred: {e}")


def delete(src, dst):
    try:
        if not dst:
            dst = IPTABLES[int(src)]
        cmd = f"iptables -t nat -D PREROUTING -p tcp --dport {src} -j REDIRECT --to-port {dst}"
        os.system(cmd)
        print(f"{src}\t{R}➤➤➤{X}\t{dst}")
    except Exception as e:
        print(f"An error occurred: {e}")

def clear():
    global IPTABLES
    for key in list(IPTABLES.keys()):
        value = IPTABLES[key]
        delete(key, value)
        del IPTABLES[key]

def main():
    print("Input Options: Add = a, Delete = d, List = l, Clear = c")
    print("Format: [a,d] src dst")
    overview()
    try:
        while True:
            input_ = input("> ")
            i = input_.split(" ")
            if "a" == i[0] and len(i) == 3:
                add(i[1], i[2])
            elif "d" == i[0] and len(i) >= 2:
                if len(i) == 2:
                    delete(i[1], None)
                else:
                    delete(i[1], i[2])
            elif input_ == "list" or input_ == "l":
                overview()
            elif input_ == "clear" or input_ == "c":
                clear()
            else:
                print("Wrong input!")
    except KeyboardInterrupt:
        print("\nExit!")

if __name__ == "__main__":
    main()