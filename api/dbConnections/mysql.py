import logging
import pandas as pd
from dbConnections.utils import limitSql

logger = logging.getLogger(__name__)


class MySQL:
    """
    Class to support functionalities on MySQL connection
    """

    def checkConnection(params):
        """ Function to connect mysql db """
        from MySQLdb import connect

        res = True
        try:
            host = params.get("host", "")
            port = int(params.get("port", 25060))
            database = params.get("database", "")
            username = params.get("username", "")
            password = params.get("password", "")
            conn = connect(
                host=host, port=port, db=database, user=username, password=password
            )

        except Exception as ex:
            logger.error("Can't connect to db with this credentials %s",str(ex))
            res = False
        return res

    def fetchDataframe(params: str, sql: str, limit: bool = False):
        """ Function to fetch data from mysql db """
        from MySQLdb import connect

        dataframe = None
        try:
            host = params.get("host", "")
            port = int(params.get("port", 25060))
            database = params.get("database", "")
            username = params.get("username", "")
            password = params.get("password", "")
            conn = connect(
                host=host, port=port, db=database, user=username, password=password
            )
            if limit:
                sql = limitSql(sql)
            chunksize = None
            dataframe = pd.read_sql(sql, conn, chunksize=chunksize)

        except Exception as ex:
            logger.error("Can't connect to db with this credentials %s", str(ex))

        return dataframe
