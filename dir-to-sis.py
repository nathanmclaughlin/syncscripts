#!/usr/bin/env python
# totally a work in progress

"""Script to gather IMDB keywords from 2013's top grossing movies."""
import sys

URL = "http://www.imdb.com/search/title?at=0&sort=boxoffice_gross_us,desc&start=1&year=2013,2013"

def main():
    """Main entry point for the script."""
    pass

def get_top_grossing_movie_links(url):
    """Return a list of tuples containing the top grossing movies of 2013 and link to their IMDB
    page."""
    pass

def get_keywords_for_movie(url):
    """Return a list of keywords associated with *movie*."""
    pass

if __name__ == '__main__':
    sys.exit(main())
import pyodbc, ldap, ldaphelper, csv, ConfigParser

ini = 'config.ini'
config = ConfigParser.SafeConfigParser()
config.read(ini)

baseDN = 'ou=StudentAccounts,o=kps'
searchScope = ldap.SCOPE_SUBTREE
retrieveAttributes = ['studentID', 'cn', 'mail'] 
searchFilter = '(&(objectClass=user)(studentID=*)(mail=*))'

emailList = {}

try:
    l = ldap.initialize(config.get('Directory','server'))
    l.protocol_version = ldap.VERSION3  
except ldap.LDAPError, e:
    print e

try:
    l.simple_bind_s(config.get('Directory','user'), config.get('Directory','password'))
except ldap.LDAPError, e:
    print e

try:
    r = l.search_s(baseDN, searchScope, searchFilter, retrieveAttributes)
    res = ldaphelper.get_search_results(r)
    for record in res:
        mail = record.get_attr_values('mail')[0]
        mail = mail.lower()
        if record.has_attribute('studentID'):
            id = record.get_attr_values('studentID')[0]
            emailList[id] = mail

except ldap.LDAPError, e:
    print e


sql = open(config.get('SQL','compass-students')).read()

try:
	conn = pyodbc.connect(config.get('StudentDB','conn'))
except pyodbc.Error, e:
	print e

outFile = open('kps-students.csv', 'wb')
outWriter = csv.writer(outFile, delimiter=',', quotechar='"')
outHeader = ['firstname','lastname','mail','phone','title','location','dept']
outWriter.writerow(outHeader)

cur = conn.cursor()
cur.execute(sql)

for row in cur.fetchall():
    line = list(row)
    id = str(line[0])
    # fname, lname, email, phone, position, location, department
    fname = line[2].title()
    lname = line[1].title()
    # email lookup via id
    if id in emailList:
        email = emailList[id]
    else:
        email = ''
    # phone lookup via location
    try:
        phone = config.get('Phone', line[5])
    except:
        phone = '269-337-0100'
    # position lookup via
    position = config.get('Position', line[9])
    # location lookup
    location = config.get('Location', line[5])
    # department lookup
    try:
       department = config.get('Department', line[5])
    except:
        department = ''

    # print id, fname, lname, email, phone, position, location, department
    outLine = [fname, lname, email, phone, position, location, department]
    outWriter.writerow(outLine)


conn.close()
outFile.close()
