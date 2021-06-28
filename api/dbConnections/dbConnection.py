import json
import logging
from django.db import connection
from google.cloud import bigquery
from google.oauth2 import service_account
from anomaly.models import Connection

logger = logging.getLogger(__name__)

class BigQueryConnection:

    def bigQueryConnection(file):
        """
        Connection for bigQuery database
        """
        res = True
        try:
            file = json.loads(file)
            service_account_info = file
            credentials = service_account.Credentials.from_service_account_info(service_account_info)
            project_id= file.get("project_id")
            client = bigquery.Client(credentials= credentials,project=project_id)
        except Exception as ex:
            logger.error("Can't connect to db with this credentials %s", str(ex))
            res = False

        return res



