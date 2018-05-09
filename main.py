import pymssql
import json
import pandas as pd
import optparse 
import xmltodict
import os
from sqlalchemy.orm import sessionmaker

from cctmodels import create_table, sdb_connect, mdb_connect
from pipeline import WritePatientData


server = '0.0.0.0'
user = 'SA'
password = 'change-this-to-real-password'
port = 1433
dbname = 'medicine'

conn = pymssql.connect(server, user, password, dbname, port = port)



parser = optparse.OptionParser()

parser.add_option(
	"-i", "--data_source", default='other',
	help="read data from mssql or pickle"
)

parser.add_option(
	"-p", "--pickle", default="False",
	help="pickle the table from mssql or not"
)

parser.add_option(
	"-o", "--to_db", default="mysql",
	help="to mysql or sqlite"
)


if __name__=="__main__":

	root = os.getcwd() + '/'
	opts = parser.parse_args()[0]

	if opts.data_source == 'mssql':
		print('Reading the Table from MS-sql-server! ')
		df = pd.read_sql('select * from xml_table', conn)

		if opts.pickle:
			print("Pickle the Data to:", root + 'data/xml.p')
			df.to_pickle(root + 'data/xml.p')
	
	else:
		print('Load Data from Pickle:', root + 'data/xml.p')
		df = pd.read_pickle(root + 'data/xml.p')

	# MySQL
	# create database cctdb character set utf8 collate utf8_general_ci;
	if opts.to_db == 'mysql':
		print('generating MySQL DB')
		engine = mdb_connect()
	else:
		print('generating SQLite')
		engine = sdb_connect(os.getcwd())

	create_table(engine)
	Session = sessionmaker(bind = engine)
	session = Session()

	for ind, dt in df.iterrows():
		dt_dict = dt.to_dict()
		dt_dict['Data'] = xmltodict.parse(dt_dict['Data'] )
		WritePatientData(dt_dict, session)