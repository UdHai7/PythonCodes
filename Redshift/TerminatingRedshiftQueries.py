#!/usr/bin/python
import csv,sys
import os
import traceback
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


mart_db_host = os.environ.get('MART_DB_HOST')
mart_db_name = os.environ.get('MART_DB_NAME')
mart_db_username = os.environ.get('MART_DB_USERNAME')
mart_db_password = os.environ.get('MART_DB_PASSWORD')


conn_string = "dbname='template1' user='{0}' host='{1}' password='{2}' port='5439'".format(mart_db_username,mart_db_host,mart_db_password)
print conn_string
con = psycopg2.connect(conn_string)

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = con.cursor()
try:
	# for log out existing users
	query = "select pid, trim(user_name) as user, starttime, query , substring(query,1,20), status from stv_recents where status='Running'"
	print "current sessions query: ", query
	cur.execute(query)
	records = cur.fetchall()
	print records
	for record in records:
		term_query = "select pg_terminate_backend(" + str(record[1]) + ")"
	 	print term_query
		cur.execute(term_query)
		print "Query Executed successfully",term_query
except psycopg2.ProgrammingError as err:
    print traceback.format_exception_only(type(err), err)
    # print 'database {0} does not exist'.format(mart_db_name)
except psycopg2.OperationalError  as op_err:
    print traceback.format_exception_only(type(op_err), op_err)

cur.close()
con.close()
