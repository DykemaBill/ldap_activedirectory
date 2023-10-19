## Python-LDAP library
## pip3 install python-ldap
## Masked password input
## pip3 install pwinput

import sys, ldap, ldap.resiter, pwinput

class LDAP(ldap.ldapobject.LDAPObject,ldap.resiter.ResultProcessor):
  pass

def ldap_login(conn_ldap, domain, account, password):
    print ("Domain: " + str(domain))
    try:
        conn_ldap.simple_bind_s(account + "@" + domain, password)
        print("Logged in!")
        return True
    except:
        print("Login failed!")
        return False

def ldap_search(conn_ldap, ad_forest, search_term):
    if (len(search_term) < 1) or (search_term == "*"):
        search_term = ""
    else:
        search_term = search_term + "*"
    search_response = conn_ldap.search(ad_forest, ldap.SCOPE_SUBTREE, "CN=*" + search_term)
    for res_type, res_data, res_msgid, res_controls in conn_ldap.allresults(search_response):
        for dn, entry in res_data:
            #print(dn,entry['objectClass'])
            print(dn,entry)

# Get command line arguments
if __name__ == "__main__":
    if len(sys.argv) == 3:
        ad_server = sys.argv[1]
        ad_domain = sys.argv[2]
        ad_forest = "dc=" + ad_domain.split(".")[0] + ",dc=" + ad_domain.split(".")[1]
        # LDAP setup
        #conn_ldap = ldap.initialize("ldap://" + server) # Without class creation to bring in resiter for search
        ad_conn_ldap = LDAP("ldap://" + ad_server)
        ad_conn_ldap.set_option(ldap.OPT_REFERRALS, 0)
        # Read login
        ad_acct = input("Active Directory account ID: ")
        ad_pass = pwinput.pwinput(prompt="Active Directory password: ")
        # Login
        login_successful = ldap_login(ad_conn_ldap, ad_domain, ad_acct, ad_pass)
        if login_successful:
            # Read search term
            ad_search = input("Term to search for: ")
            # Search
            ldap_search(ad_conn_ldap, ad_forest, ad_search)
    else:
        print ("Syntax:")
        print ("        " + sys.argv[0] + " [AD server] [AD domain in domain.ext format]")