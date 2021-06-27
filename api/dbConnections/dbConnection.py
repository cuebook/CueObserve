import json

from django.db import connection
from google.cloud import bigquery
from google.oauth2 import service_account
from anomaly.models import Connection

class BigQueryConnection:

    def bigQueryConnection(file):
        """
        Connection for bigQuery database
        """
        file = Connection.objects.filter(connectionType_id=4)[0].file
        file = json.loads(file)
        service_account_info = file
        credentials = service_account.Credentials.from_service_account_info(service_account_info)
        project_id= file.get("project_id")
        client = bigquery.Client(credentials= credentials,project=project_id)

        return client



