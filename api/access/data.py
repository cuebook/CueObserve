
import dbConnections
from anomaly.serializers import ConnectionDetailSerializer


class Data:
    @staticmethod
    def runQueryOnConnection(connectionType, connectionParams, query, limit=True):
        dataframe = None
        if connectionType == "BigQuery":
            params = connectionParams
            dataframe = dbConnections.BigQuery.fetchDataframe(params, query, limit=limit)
        if connectionType == "Druid":
            params = connectionParams
            dataframe = dbConnections.Druid.fetchDataframe(params, query, limit=limit)
        if connectionType == "MySQL":
            params = connectionParams
            dataframe = dbConnections.MySQL.fetchDataframe(params, query, limit=limit)
        if connectionType == "Postgres":
            params = connectionParams
            dataframe = dbConnections.Postgres.fetchDataframe(params, query, limit=limit)
        if connectionType == "MSSQL":
            params = connectionParams
            dataframe = dbConnections.MSSQL.fetchDataframe(params, query, limit=limit)

        if connectionType == "Redshift":
            params = connectionParams
            dataframe = dbConnections.Redshift.fetchDataframe(params, query, limit=limit)
        if connectionType == "Snowflake":
            params = connectionParams
            dataframe = dbConnections.Snowflake.fetchDataframe(params, query, limit=limit)
        if connectionType == "ClickHouse":
            params = connectionParams
            dataframe = dbConnections.ClickHouse.fetchDataframe(params, query, limit=limit)

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
