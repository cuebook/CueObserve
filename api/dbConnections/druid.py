from pydruid.db import connect
from dbConnections.utils import limitSql
import json
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class Druid:
    """
    Class to support functionalities on Druid connection
    """
    def checkConnection(params):
        res = True
        try:
            host = params.get("host", "")
            port = params.get("port", 8888)
            conn = connect(
            host=host,
            port=port,
            path="/druid/v2/sql/",
            scheme="http"
            )
            curs = conn.cursor()
            sql = "SELECT * FROM RETURNENTRY"
            sql = limitSql(sql)
            chunksize =  None
            dataframe = pd.read_sql(sql, conn, chunksize=chunksize)

        except Exception as ex:
            logger.error("Can't connect to db with this credentials ")
            res = False
        return res

    def fetchDataframe(params: str, sql: str, limit: bool = False):
        dataframe = None
        try:
            host = params.get("host", "")
            port = params.get("port", 8888)
            conn = connect(
            host=host,
            port=port,
            path="/druid/v2/sql/",
            scheme="http"
            )
            if limit:
                sql = limitSql(sql)
            chunksize =  None
            dataframe = pd.read_sql(sql, conn, chunksize=chunksize)
            
        except Exception as ex:
            logger.error("Can't connect to db with this credentials %s", str(ex))

        return dataframe
