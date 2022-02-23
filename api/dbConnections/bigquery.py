import json
import logging
from google.cloud import bigquery
from google.oauth2 import service_account

from dbConnections.utils import limitSql

logger = logging.getLogger(__name__)


class BigQuery:
    """
    Class to support functionalities on bigquery connection
    """

    @staticmethod
    def checkConnection(params: str):
        """
        Connection for bigQuery database
        :param file: credential file from bigquery to connection
        """
        res = True
        file = params.get("file", {})

        try:
            file = json.loads(file)
            service_account_info = file
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info
            )
            project_id = file.get("project_id")
            client = bigquery.Client(credentials=credentials, project=project_id)
        except Exception as ex:
            logger.error("Can't connect to db with this credentials %s", str(ex))
            res = False

        return res

    @staticmethod
    def fetchDataframe(params: str, sql: str, limit: bool = False):
        """
        Fetches data using given config file and sql
        :param file: connection file
        :param sql: string sql query
        :param limit: limit data
        :returns: dataframe
        """
        dataframe = None
        file = params.get("file", {})
        try:
            if limit:
                sql = limitSql(sql)
            file = json.loads(file)
            service_account_info = file
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info
            )
            project_id = file.get("project_id")
            client = bigquery.Client(credentials=credentials, project=project_id)
            dataJob = client.query(sql)
            dataframe = dataJob.to_dataframe()
        except Exception as ex:
            logger.error("Error in fetching data. Error:%s", str(ex))

        return dataframe
