from dbConnections import BigQuery
from anomaly.serializers import ConnectionDetailSerializer

class Data:
    @staticmethod
    def runQueryOnConnection(connectionType, connectionParams, query, limit=True):
        dataframe = None
        if connectionType == "BigQuery":
            file = connectionParams['file']
            dataframe = BigQuery.fetchDataframe(file, query, limit=True)
        return dataframe
    
    @staticmethod
    def fetchDatasetDataframe(dataset):
        connectionData = ConnectionDetailSerializer(dataset.connection)
        datasetDf = Data.runQueryOnConnection(connectionData["connectionType"], connectionData["params"], dataset.sql, False)
        return datasetDf
    

        
