"""Export student data for Career Cruising."""

import tablib, ConfigParser, pyodbc

ini = 'config.ini'
config = ConfigParser.SafeConfigParser()
config.read(ini)

data = tablib.Dataset()

sql = open(config.get('SQL','career-cruising')).read()

try:
	conn = pyodbc.connect(config.get('StudentDB','conn'))
	cur = conn.cursor()
	cur.execute(sql)
	data.headers = [column[0] for column in cur.description]

	for row in cur.fetchall():
		data.append(row)
except pyodbc.Error, e:
	print e

with open('students.xlsx', 'wb') as f:
	f.write(data.xlsx)
