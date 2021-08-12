import pyodbc
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class MSSQL:
	"""
	Functionalities for MSSQL 
	"""

	@staticmethod
	def __getCursor(params: dict):
		"""
		Gets connection parameters
		:param params: params with keys - host, username, password
		"""
		server = params.get("host", "") 
		username = params.get("username", "")
		password = params.get("password", "")
		cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';UID='+username+';PWD='+ password)
		return cnxn

	def checkConnection(params):
		"""
		Check if connection 
		:param params: params with keys - host, username, password
		"""
		try:
			MSSQL.__getCursor(params)
			return True
		except Exception as ex:
			logger.error("Can't connect to ")
			return False

	def fetchDataframe(params: dict, sql: str, limit: bool = False):
		"""
		Fetch data for sql using given params
		:param params: params with keys - host, username, password
		:param sql: sql string 
		:param limit: if limited data to be fetched
		"""
		dataframe = None
		try:
		    cnxn = MSSQL.__getCursor(params)
		    dataframe = pd.read_sql(sql, cnxn)
		    if limit:
		    	dataframe = dataframe[:10]
		except Exception as ex:
		    logger.error("Can't connect to db with this credentials %s", str(ex))

		return dataframe


