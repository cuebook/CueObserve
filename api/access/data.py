from dbConnections import BigQuery, Druid, Redshift, Snowflake
from anomaly.serializers import ConnectionDetailSerializer
from dbConnections import Druid, MySQL
from dbConnections.postgres import Postgres
from anomaly.services import Connections


class Data:
    @staticmethod
    def runQueryOnConnection(connectionType, connectionParams, query, limit=True):
        dataframe = None
        if connectionType == "BigQuery":
            file = connectionParams["file"]
            dataframe = BigQuery.fetchDataframe(file, query, limit=limit)
        if connectionType == "Druid":
            params = connectionParams
            dataframe = Druid.fetchDataframe(params, query, limit=limit)
        if connectionType == "MySQL":
            params = connectionParams
            dataframe = MySQL.fetchDataframe(params, query, limit=limit)
        if connectionType == "Postgres":
            params = connectionParams
            dataframe = Postgres.fetchDataframe(params, query, limit=limit)
            
        if connectionType == "Redshift":
            params = connectionParams
            dataframe = Redshift.fetchDataframe(params, query, limit=limit)
        if connectionType == "Snowflake":
            params = connectionParams
            dataframe = Snowflake.fetchDataframe(params, query, limit=limit)

        return dataframe

    @staticmethod
    def fetchDatasetDataframe(dataset):
        connectionType, connectionParams = Connections.getConnectionParams(
            dataset.connection.id
        )
        datasetDf = Data.runQueryOnConnection(
            connectionType,
            connectionParams,
            dataset.sql,
            False,
        )
        return datasetDf
