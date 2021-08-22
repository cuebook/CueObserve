import logging
import clickhouse_driver as ch

logger = logging.getLogger(__name__)


class ClickHouse:
    """
    Functionalities for ClickHouse
    """

    @staticmethod
    def __getClient(params: dict):
        """
        Gets connection parameters
        :param params: params with keys - url, host, port, username, password, database, timeout
        """
        url = params.get("url", "")
        if url != "":
            client = ch.Client.from_url(url)
        else:
            host = params.get("host", "localhost")
            port = params.get("port", "9000")
            username = params.get("user", "default")
            password = params.get("password", "")
            database = params.get("database", "default")
            timeout = params.get("timeout", "")
            params.update({
                "host": host,
                "port": port,
                "username": username,
                "password": password,
                "database": database,
            })
            if timeout != "":
                params.update({
                    "send_receive_timeout": timeout,
                    "connect_timeout": timeout,
                    "sync_requests_timeout": timeout,
                })

            client = ch.Client(settings={'use_numpy': True}, **params)
        return client

    @staticmethod
    def checkConnection(params):
        """
        Check if connection
        :param params: params with keys - host, username, password
        """
        try:
            ClickHouse.__getClient(params)
            return True
        except Exception as ex:
            logger.error("Error in connection: %s", str(ex))
            return False

    @staticmethod
    def fetchDataframe(params: dict, sql: str, limit: bool = False):
        """
        Fetch data for sql using given params
        :param params: params with keys - host, username, password
        :param sql: sql string
        :param limit: if limited data to be fetched
        """
        dataframe = None
        try:
            client = ClickHouse.__getClient(params)
            dataframe = client.query_dataframe(sql)
            if limit:
                dataframe = dataframe[:10]
        except Exception as ex:
            logger.error("Can't fetch dataframe: %s", str(ex))

        return dataframe
