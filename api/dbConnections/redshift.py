import logging
import pandas as pd
from sqlalchemy import create_engine
from dbConnections.utils import limitSql

logger = logging.getLogger(__name__)


class Redshift:
    """
    Class to support functionalities of Redshift connection
    """

    @staticmethod
    def __getEngine(params: dict):
        """
        Gets engine for redshift connection
        """
        endpoint: str = params.get("endPoint", "")
        username: str = params.get("username", "")
        password: str = params.get("password", "")

        engine = create_engine(f"postgresql://{username}:{password}@{endpoint}")
        return engine

    @staticmethod
    def checkConnection(params: dict):
        """
        Connection for Redshift database
        """
        res = True
        engine = Redshift.__getEngine(params)
        try:
            dataframe = pd.read_sql("SELECT 1", engine)
        except Exception as ex:
            logger.error(str(ex))
            res = False
        return res

    @staticmethod
    def fetchDataframe(params, sql: str, limit: bool = False):
        """
        Fetches data using given config file and sql
        :param params: connection params
        :param sql: string sql query
        :param limit: limit data
        :returns: dataframe
        """
        dataframe = None
        try:
            engine = Redshift.__getEngine(params)
            if limit:
                sql = limitSql(sql)
            dataframe = pd.read_sql(sql, engine)
        except Exception as ex:
            logger.error("Can't connect to db with this credentials %s", str(ex))

        return dataframe
