import json
import logging
from django.db import connection
from google.cloud import bigquery
from google.oauth2 import service_account

logger = logging.getLogger(__name__)


class BigQuery:
    def checkConnection(file):
        """
        Connection for bigQuery database
        """
        res = True
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

    def fetchDataframe(file, sql, limit=False):
        """
        Fetches data using given config file and sql
        """
        dataframe = None
        try:
            file = json.loads(file)
            service_account_info = file
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info
            )
            project_id = file.get("project_id")
            client = bigquery.Client(credentials=credentials, project=project_id)
            dataJob = client.query(sql)
            dataframe = dataJob.to_dataframe()
            if limit:
                dataframe = dataframe[:10]
        except Exception as ex:
            logger.error("Can't connect to db with this credentials %s", str(ex))

        return dataframe
