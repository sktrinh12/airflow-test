import datetime

from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator
from airflow.hooks.postgres_hook import PostgresHook
#import cx_Oracle
from airflow.providers.oracle.hooks.oracle import OracleHook

#class OracleConnection(object):
#	def __init__(self, username, password, hostname, port):
#		self.username = username
#		self.password = password
#		self.hostname = hostname
#		self.port = port
#
#	def __enter__(self):
#		try:
#			dsn = f"""(DESCRIPTION=
#					(ADDRESS=(PROTOCOL=TCP)(HOST="{self.hostname})(PORT={self.port}))
#					(CONNECT_DATA=(GLOBAL_NAME=HPP1.WORLD)(SID=HPP1)))"""
#			self.con = cx_Oracle.connect(user=self.username, password=self.password, dsn=dsn, encoding="UTF-8")
#			return self.con
#		except cx_Oracle.DatabaseError as e:
#			raise
#
#	def __exit__(self, exc_type, exc_val, exc_tb):
#		try:
#			self.con.close()
#		except cx_Oracle.DatabaseError:
#			pass

def exe_query_pgsql_hook():
	hook = PostgresHook(postgres_conn_id="postgres_azure")
	df = hook.get_pandas_df(sql='SELECT * FROM TESTDB2')
	print(df.to_string())

def exe_query_oracle_hook():
	hook = OracleHook(oracle_conn_id="oracle_halfpipe")
	df = hook.get_pandas_df(sql='SELECT SAPCLONENAME FROM VWAUTOMATIONDATA WHERE ROWNUM < 4')
	print(df.to_string())
	if df.shape[0] > 1:
		print(f'{df.shape[0]} rows - there are new clones')

#def exe_query_oracle():
#	with OracleConnection("TRINH", "LXR0;?5wdYsMlSZ", "hpp1db.global.bdx.com", 7359) as conn:
#		sql_stmt = "SELECT SAPCLONENAME FROM VWAUTOMATIONDATA WHERE ROWNUM < 4"
#		df = pd.read_sql(sql_stmt, con=conn)
#		print(df.to_string())
	

with DAG(
	dag_id="postgres_operator_dag",
	start_date=datetime.datetime.now(),
	schedule_interval="@once",
	catchup=False,
	) as dag:
		python_pgsql_call = PythonOperator(
			task_id='pgsql_call',
			provide_context=True,
			python_callable=exe_query_pgsql_hook
		)
		python_oracle_call = PythonOperator(
			task_id='oracle_call',
			provide_context=True,
			python_callable=exe_query_oracle_hook
		)
		
python_pgsql_call >> python_oracle_call
