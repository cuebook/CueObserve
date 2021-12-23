import json
import logging
import pandas as pd
from pydruid.db import connect
from dbConnections.utils import limitSql

logger = logging.getLogger(__name__)


class Druid:
    """
    Class to support functionalities on Druid connection
    """

    @staticmethod
    def checkConnection(params):
        """
        Check if connection can be esatblished for druid
        """
        res = True
        try:
            host = params.get("host", "")
            port = params.get("port", 8888)
            conn = connect(host=host, port=port, path="/druid/v2/sql/", scheme="http")
            curs = conn.cursor()
            dataframe = pd.read_sql("SELECT 1", conn, chunksize=None)

        except Exception as ex:
            logger.error("Can't connect to db with this credentials ")
            res = False
        return res

    @staticmethod
    def fetchDataframe(params: dict, sql: str, limit: bool = False):
        """
        Fetch dataframe for given sql
        """
        dataframe = None
        try:
            host = params.get("host", "")
            port = params.get("port", 8888)
            conn = connect(host=host, port=port, path="/druid/v2/sql/", scheme="http")
            if limit:
                sql = limitSql(sql)
            chunksize = None
            dataframe = pd.read_sql(sql, conn, chunksize=chunksize)

        except Exception as ex:
            logger.error("Can't connect to db with this credentials %s", str(ex))

        return dataframe
