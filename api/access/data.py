from dbConnections import BigQuery, Druid, Redshift, Snowflake
from anomaly.serializers import ConnectionDetailSerializer
from dbConnections import Druid, MySQL
from dbConnections.postgres import Postgres


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
        connectionParams = {}
        for val in dataset.connection.cpvc.all():
            connectionParams[val.connectionParam.name] = val.value
        datasetDf = Data.runQueryOnConnection(
            dataset.connection.connectionType.name,
            connectionParams,
            dataset.sql,
            False,
        )
        return datasetDf
