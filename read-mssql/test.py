import pymssql
import json
import pandas as pd

server = '0.0.0.0'
user = 'SA'
password = 'change-this-to-real-password'
port = 1433
dbname = 'medicine'

conn = pymssql.connect(server, user, password, dbname, port = port)

root = '/home/floyd/Desktop/luohudb/'

df = pd.read_sql('select * from xml_table', conn)
df.to_pickle(root + 'data/xml.p')

