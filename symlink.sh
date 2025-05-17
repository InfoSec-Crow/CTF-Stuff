#!/bin/bash

# Scripts
sudo ln -s /opt/CTF-Stuff/scripts/makepl/makepl.py /usr/local/bin/makepl
chmod +x /usr/local/bin/makepl
sudo ln -s /opt/CTF-Stuff/scripts/server/s.py /usr/local/bin/s
chmod +x /opt/CTF-Stuff/scripts/server/s.py
sudo ln -s /opt/CTF-Stuff/scripts/ssh_/ssh_.py /usr/local/bin/ssh_
chmod +x /opt/CTF-Stuff/scripts/ssh_/ssh_.py

# Setup
sudo ln -s /opt/CTF-Stuff/setup/ctf/start_ctf.py /usr/local/bin/start_ctf
