from dbConnections import BigQuery, Druid, Redshift, Snowflake
from anomaly.serializers import ConnectionDetailSerializer
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
