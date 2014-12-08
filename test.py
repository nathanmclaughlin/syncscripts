"""Playing with tablib. This is just a scratchpad."""

import tablib

data = tablib.Dataset()

with open('email.csv', 'r') as f:
	data.csv = f.read()

print data.dict

#with open('test.csv', 'wb') as f:
#	f.write(data.csv)