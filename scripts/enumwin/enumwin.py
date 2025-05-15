#!/usr/bin/python3
from impacket.ldap import ldap
from impacket.ldap.ldapasn1 import SearchResultReference

class ENUM_AD:
    def __init__(self, domain, username, nthash, ldap_host, base_dn):
        self.domain = domain
        self.username = username
        self.nthash = nthash
        self.ldap_host = ldap_host
        self.base_dn = base_dn
        self.ldap_connection = None

    def connect_hash(self):
        lmhash = '00000000000000000000000000000000'
        creds = {
            'username': self.username,
            'password': '',
            'domain': self.domain,
            'lmhash': lmhash,
            'nthash': self.nthash
        }
        try:
            self.ldap_connection = ldap.LDAPConnection(f'ldap://{self.ldap_host}', self.base_dn)
            self.ldap_connection.login(
                creds['username'],
                creds['password'],
                creds['domain'],
                lmhash=creds['lmhash'],
                nthash=creds['nthash']
            )
            print("[+] Successfully connected to LDAP")
        except Exception as e:
            print(f"[-] Connection error: {e}")
            sys.exit(1)

    # def query_user_attribute(self, search_filter, attributes):
    #     if not self.ldap_connection:
    #         print("[-] Not connected to LDAP")
    #         return None

    #     try:
    #         results = self.ldap_connection.search(
    #             searchFilter=search_filter,
    #             attributes=[attribute_name]
    #         )

    #         filtered_results = [entry for entry in search_results if not isinstance(entry, SearchResultReference)]
    #         return filtered_results
    #         return None
    #     except Exception as e:
    #         print(f"[-] Search error: {e}")
    #         return None
            

    def query(self, search_filter, attributes):
        if not self.ldap_connection:
            print("[-] Not connected to LDAP")
            return 0
        try:
            search_results = self.ldap_connection.search(
                searchFilter=search_filter,
                attributes=attributes
            )
            filtered_results = [entry for entry in search_results if not isinstance(entry, SearchResultReference)]
            return filtered_results
            
        except Exception as e:
            print(f"[-] Search error: {e}")
            return 0

    def count_users(self):
        #result = self.query('(objectClass=user)', ['distinguishedName'])
        results = self.query('(objectClass=user)', ['name'])
        
        print(f"[+] Number of users: {len(results)}")
        for entry in results:
            for attribute in entry['attributes']:
                # attribute['type']
                print(f"{attribute['vals'][0]}")
            


if __name__ == "__main__":
    domain = 'scepter.htb'
    username = 'd.baker'
    nthash = '18b5fb0d99e7a475316213c15b6f22ce'
    ldap_host = 'dc01.scepter.htb'
    base_dn = 'DC=scepter,DC=htb'

    ldap_con = ENUM_AD(domain, username, nthash, ldap_host, base_dn)
    ldap_con.connect_hash()
    ldap_con.count_users()

    #search_filter = f'(sAMAccountName={username})'
