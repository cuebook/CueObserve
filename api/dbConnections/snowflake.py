import logging
import snowflake.connector  # pylint: disable=E0611, E0401
import pandas as pd
from dbConnections.utils import limitSql

logger = logging.getLogger(__name__)


class Snowflake:
    """
    Class to support functionalities of Snowflake connection
    """

    @staticmethod
    def __getConnector(params: dict):
        """
        Gets snowflake connector
        """
        user: str = params.get("username", "")
        password: str = params.get("password", "")
        account: str = params.get("account", "")

        ctx = snowflake.connector.connect(  # pylint: disable=E1101
            user=user, password=password, account=account
        )
        return ctx

    @staticmethod
    def checkConnection(params: dict):
        """
        Connection for Snowflake database
        """
        res = True
        try:
            Snowflake.__getConnector(params)
        except Exception as ex:
            logger.error(str(ex))
            res = False
        return res

    @staticmethod
    def fetchDataframe(params, sql: str, limit: bool = False):
        """
        Fetches data using given config file and sql
        :param file: connection file
        :param sql: string sql query
        :param limit: limit data
        :returns: dataframe
        """
        dataframe = None
        try:
            ctx = Snowflake.__getConnector(params)
            if limit:
                sql = limitSql(sql)
            dataframe = pd.read_sql(sql, ctx)
        except Exception as ex:
            logger.error("Can't connect to db with this credentials %s", str(ex))

        return dataframe
