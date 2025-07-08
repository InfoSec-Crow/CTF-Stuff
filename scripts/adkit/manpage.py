
info = '''
[Protocol]
smb\t= view smb shares & files
winrm\t= login to winrm (cmd)
ldap\t= login to ldap (query)

[Enumeration]
krb\t= generate krb config file
bh\t= collect bloodhound data
dele\t= find delegation
sid\t= show all domain sids

[Lists]
user\t= list all usernames
group\t= list all groups
computer = list all computers

[DACL]
acl\t= list dacl
gadd\t= add user to group
glist\t= list groups from user
gremove\t= remove user from group
edit\t= set dacl FullControl
wspn\t= write spn
active\t= activate account
wowner\t= write owner
rowner\t= read owner
cadd\t= add computer

[Attack]
aroast\t= asreproasting
kroast\t= kerberoasting
tkroast = target kerberoasting
chpw\t= ForceChangePassword
sc\t= Shadow Credentials
gmsa\t= ReadGMSAPassword
laps\t= ReadLAPSPassword
dcsync\t= DCSync
gold\t= Golden Ticket
silver\t= Silver Ticket
rbcd\t= Resource-Based Constrained Delegation

[ADCS]
vulntemp = find vuln CertTemp
esc1\t= ESC1
esc2\t= ESC2
esc3\t= ESC3
esc4\t= ESC4
'''
