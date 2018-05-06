import pymssql
import json
import pandas as pd

server = '127.0.0.1'
user = 'SA'
password = '<YourStrong!Passw0rd>'
conn = pymssql.connect(server, user, password, "newcct", port = 1401)



df = pd.read_sql('select * from xml_table', conn)

a = df
print df.head()

a2 = a.to_json(orient = 'split')
# print a2
print type(a2)


with open('xml.json',  'w') as f:
	f.write(a2)

