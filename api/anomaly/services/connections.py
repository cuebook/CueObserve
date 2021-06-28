import logging
from typing import List
from utils.apiResponse import ApiResponse
from dbConnections.dbConnection import BigQueryConnection
from anomaly.models import Connection, ConnectionParam, ConnectionType, ConnectionParamValue
from anomaly.serializers import ConnectionSerializer, ConnectionDetailSerializer, ConnectionTypeSerializer

# Get an instance of a logger
logger = logging.getLogger(__name__)

class Connections:

    @staticmethod
    def getConnections():
        res = ApiResponse()
        connections = Connection.objects.all()
        serializer = ConnectionSerializer(connections, many=True)
        res.update(True, "Connections retrieved successfully", serializer.data)
        return res

    @staticmethod
    def getConnection(connection_id):
        res = ApiResponse()
        connections = Connection.objects.get(id=connection_id)
        serializer = ConnectionDetailSerializer(connections)
        res.update(True, "Connection retrieved successfully", serializer.data)
        return res

    @staticmethod
    def addConnection(payload):
        connectionResponse = False
        res = ApiResponse()
        connectionType = ConnectionType.objects.get(id=payload["connectionType_id"])
        file = payload["params"].get("file",{})  #now it's only for BigQuery connection
        if payload["connectionType_id"] == 4:
            connectionResponse = BigQueryConnection.bigQueryConnection(file)

            if connectionResponse:
                connection = Connection.objects.create(
                    name=payload["name"], description=payload["description"], connectionType=connectionType, file=file
                )
                for param in payload["params"]:
                    cp = ConnectionParam.objects.get(name=param, connectionType=connectionType)
                    ConnectionParamValue.objects.create(
                        connectionParam=cp, value=payload["params"][param], connection=connection
                    )
           
                res.update(True, "Connection added successfully")
            else:
                logger.error("DB connection failed :")
                res.update(False, "Connection Failed")

        else:
            connection = Connection.objects.create(
                    name=payload["name"], description=payload["description"], connectionType=connectionType, file=file
                )
            for param in payload["params"]:
                cp = ConnectionParam.objects.get(name=param, connectionType=connectionType)
                ConnectionParamValue.objects.create(
                    connectionParam=cp, value=payload["params"][param], connection=connection
                )
            res.update(True, "Connection added successfully")

        return res

    @staticmethod
    def removeConnection(connection_id):
        res = ApiResponse()
        connection = Connection.objects.filter(id=connection_id)
        if len(connection)>0:
            Connection.objects.get(id=connection_id).delete()
            res.update(True, "Connection deleted successfully")
        else:
            res.update(False, "Cannot delete connection because of dependent notebook")
        return res

    @staticmethod
    def updateConnection(connection_id, payload):
        res = ApiResponse()
        Connection.objects.filter(id=connection_id).update(
            name=payload.get("name", ""),
            description=payload.get("description", ""),
            connectionType=ConnectionType.objects.get(id=payload["connectionType_id"]),
        )
        connection = Connection.objects.get(id=connection_id)
        # TODO: delete params related to this & then update
        for param in payload["params"]:
            cp = ConnectionParam.objects.get(id=param["paramId"])
            # if cp.isEncrypted:
            #     encryptionObject= AESCipher()
            #     param['paramValue'] = encryptionObject.encrypt(param['paramValue'])
            ConnectionParamValue.objects.create(
                connectionParam=cp, value=param["paramValue"], connection=connection
            )

        res.update(True, "Connection updated successfully")
        return res

    @staticmethod
    def getConnectionTypes():
        res = ApiResponse()
        connectionTypes = ConnectionType.objects.all()
        data = serializer = ConnectionTypeSerializer(connectionTypes, many=True).data
        res.update(True, "Successfully retrieved connection types", data)
        return res
