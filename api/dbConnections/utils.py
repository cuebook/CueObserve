"""
Contains utility functions for various database connections
"""
from copy import copy 
import re

def limitSql(sql: str):
	"""Appends 'LIMIT 10' to sql"""

	# replacing "limit 293849" with "limit 10"
	pattern = '(?i)(limit)[\s]+[0-9]+'
	replace = 'limit 10'
	sql = re.sub(pattern, replace, sql)

	if "limit " in sql.lower():
		return sql
	# sql = copy(sql)
	sql = sql + " limit 10"
	return sql
