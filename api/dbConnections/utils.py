"""
Contains utility functions for various database connections
"""
from copy import copy
import re


def limitSql(sql: str):
    """Appends 'LIMIT 10' to sql"""

    # replacing last matching ~ "limit 293849" with "limit 10"
    reversePattern = "[0-9]+[\s]+(?i)(timil)"
    reverseSql = sql[::-1]
    replace = "limit 10"[::-1]
    sql = re.sub(reversePattern, replace, reverseSql, 1)[::-1]

    if "limit " in sql.lower():
        return sql
    # sql = copy(sql)
    sql = sql + " limit 10"
    return sql
