
info = '''
[Protocol]
smb = view smb shares & files
winrm = login to winrm (cmd)
ldap = login to ldap (query)

[Enumeration]
krb = generate krb config file
bh = collect bloodhound data
dele = find delegation
sid = show all domain sids

[Lists]
user = list all usernames
computer = list all computers
group = list all groups

[DACL]
acl = show acl\t(impacket)
gadd = add user to group\t(bloodyad)
glist = list groups from user\t(bloodyad)
gremove = remove user from group\t(bloodyad)
edit = set dacl FullControl\t(impacket)
wspn = write spn\t(krbrelayx)
active = activate account\t(bloodyad)
wowner = write owner\t(impacket)
rowner = read owner\t(impacket)

[Attacks]
aroast = asreproasting\t(nxc)
kroast = kerberoasting\t(nxc)
kroast-imp = kerberoasting only one user\t(impacket)
chpw = ForceChangePassword\t(bloodyad)
sc = Shadow Credentials\t(certipy)
gmsa = ReadGMSAPassword\t(nxc)
laps = ReadLAPSPassword\t(impacket)
dcsync = DCSync\t(impacket)
gold = Golden Ticket\t(impacket)
silver = Silver Ticket\t(impacket)

[ADCS]
vulntemp = find vuln CertTemp\t(certipy)
esc1 = ESC1\t(certipy)
esc2 = ESC2\t(certipy)
esc3 = ESC3\t(certipy)
esc4 = ESC4\t(certipy)
'''

# [Protocol]

def smb_view():
    print("""
Action:\tsmb
Tools:\tnxc, impacket
Desc:\ttest 
""")
    exit(0)
