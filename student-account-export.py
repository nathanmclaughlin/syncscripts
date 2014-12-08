"""Export directory information in LDAP for import into eSchoolPLUS"""

import tablib, ConfigParser, ldap, ldaphelper, pyodbc

ini = 'config.ini'
config = ConfigParser.SafeConfigParser()
config.read(ini)

data = tablib.Dataset()

baseDN = 'ou=StudentAccounts,o=kps'
searchScope = ldap.SCOPE_SUBTREE
retrieveAttributes = ['studentID', 'cn', 'mail'] 
searchFilter = '(&(objectClass=user)(studentID=*)(mail=*))'

try:
	contactIDs = {}
	conn = pyodbc.connect(config.get('StudentDB','conn'))
	sql = open(config.get('SQL','student-contact-ids')).read()
	cur = conn.cursor()
	cur.execute(sql)
	for row in cur.fetchall():
		contactIDs[row.STUDENT_ID] = row.CONTACT_ID
except pyodbc.Error, e:
	print e

badidcount = 0

try:
    l = ldap.initialize(config.get('Directory','server'))
    l.protocol_version = ldap.VERSION3
    l.simple_bind_s(config.get('Directory','user'), config.get('Directory','password'))
    r = l.search_s(baseDN, searchScope, searchFilter, retrieveAttributes)
    res = ldaphelper.get_search_results(r)
    data.headers = ['CONTACT_ID','EMAIL','LOGIN_ID']
    for record in res:
        mail = record.get_attr_values('mail')[0]
        mail = mail.lower()
        cn = record.get_attr_values('cn')[0]
        cn = cn.lower()
        id = record.get_attr_values('studentID')[0]
        try:
        	contactID = contactIDs[id]
        	data.append([contactID, mail, cn])
        except:
        	# print "Not a valid student ID:", id
        	badidcount = badidcount + 1
except ldap.LDAPError, e:
    print e

print badidcount, "students in directory, but not active in eSchoolPLUS."

with open('email.csv', 'wb') as outfile:
	outfile.write(data.csv)
