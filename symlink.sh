#!/bin/bash

# Scripts
sudo ln -s /opt/CTF-Stuff/scripts/makepl/makepl.py /usr/local/bin/makepl
chmod +x /usr/local/bin/makepl

sudo ln -s /opt/CTF-Stuff/scripts/server/s.py /usr/local/bin/s
chmod +x /opt/CTF-Stuff/scripts/server/s.py

sudo ln -s /opt/CTF-Stuff/scripts/ssh_/ssh_.py /usr/local/bin/ssh_
chmod +x /opt/CTF-Stuff/scripts/ssh_/ssh_.py

sudo ln -s /opt/CTF-Stuff/scripts/adkit/adkit.py /usr/local/bin/adkit
chmod +x /opt/CTF-Stuff/scripts/adkit/adkit.py 

sudo ln -s /opt/CTF-Stuff/scripts/time_sync/t.py /usr/local/bin/t
chmod +x /opt/CTF-Stuff/scripts/time_sync/t.py

sudo ln -s /opt/CTF-Stuff/scripts/bloodhound-api/bh-api.py /usr/local/bin/bh-api
chmod +x /opt/CTF-Stuff/scripts/bloodhound-api/bh-api.py



# Setup
sudo ln -s /opt/CTF-Stuff/setup/ctf/start_ctf.py /usr/local/bin/start_ctf
chmod +x /opt/CTF-Stuff/setup/ctf/start_ctf.py
