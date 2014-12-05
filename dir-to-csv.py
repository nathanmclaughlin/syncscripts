"""Script to export network account information in LDAP to a CSV file"""

import sys, csv, ldap, ldaphelper

"""Will get these from the command line"""
accountType = "student"
if accountType == "student":
    baseDN = 'ou=StudentAccounts,o=kps'
    retrieveAttributes = ['studentID', 'cn', 'mail'] 
    searchFilter = '(&(objectClass=user)(studentID=*)(mail=*))'
else:
    baseDN = 'o=kps'
    retrieveAttributes = ['workforceID', 'cn', 'mail'] 
    searchFilter = '(&(objectClass=user)(workforceID=*)(mail=*))'

def get_account_info(accountType,baseDN,user,password):
    """Return a list of accounts with attributes."""
    accounts = []
    searchScope = ldap.SCOPE_SUBTREE
    try:
        l = ldap.initialize('ldap://ldap1.kps')
        l.protocol_version = ldap.VERSION3
        l.simple_bind_s(user, password)
        r = l.search_s(baseDN, searchScope, searchFilter, retrieveAttributes)
        res = ldaphelper.get_search_results(r)
        for record in res:
            cn = record.get_attr_values('cn')[0]
            cn = cn.lower()
            mail = record.get_attr_values('mail')[0]
            mail = mail.lower()
            id = record.get_attr_values('studentID')[0]
            accounts.append(id,cn,email)
    except ldap.LDAPError, e:
        print e
    return accounts

def usage():
    """Display proper command line usage of script."""
    pass

def main(argv):
    """Main entry point for the script."""
    try:                                
        opts, args = getopt.getopt(argv, "hg:d", ["help", "grammar="])
    except getopt.GetoptError:           3
        usage()                          4
        sys.exit(2)      

    accounts = get_account_info(type)
    with open('accounts.csv', 'w') as output:
        csvwriter = csv.writer(output)
        for id, cn, mail in accounts:
            csvwriter.writerow([id, cn, mail])


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
