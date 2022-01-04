import logging
from typing import List
from utils.apiResponse import ApiResponse
import dbConnections
from anomaly.models import (
    Connection,
    ConnectionParam,
    ConnectionType,
    ConnectionParamValue,
)
from anomaly.serializers import (
    ConnectionSerializer,
    ConnectionDetailSerializer,
    ConnectionTypeSerializer,
)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Connections:
    @staticmethod
    def getConnections():
        """
        Gets all created connections
        """
        res = ApiResponse("Error in fetching connections")
        connections = Connection.objects.all()
        serializer = ConnectionSerializer(connections, many=True)
        res.update(True, "Connections retrieved successfully", serializer.data)
        return res

    @staticmethod
    def getConnection(connection_id):
        """
        Gets connection details of given connection_id
        """
        res = ApiResponse("Error in fetching connection")
        connections = Connection.objects.get(id=connection_id)
        serializer = ConnectionDetailSerializer(connections)
        res.update(True, "Connection retrieved successfully", serializer.data)
        return res

    @staticmethod
    def getConnectionParams(connection_id):
        """
        Gets connection details of given connection_id
        """
        connection = Connection.objects.get(id=connection_id)
        params = {}
        for val in connection.cpvc.all():
            params[val.connectionParam.name] = val.value
        return connection.connectionType.name, params

    @staticmethod
    def addConnection(payload):
        """
        Add connection or build new connection
        :param payload: Contains name, connectionType_id, params, description
        """
        connectionResponse = False
        res = ApiResponse("Error in adding connection")
        connectionType = ConnectionType.objects.get(id=payload["connectionType_id"])
        connectionName = connectionType.name

        # Do this verification using Querys service

        if connectionName == "BigQuery":
            connectionResponse = dbConnections.BigQuery.checkConnection(payload["params"])
        elif connectionName == "Redshift":
            connectionResponse = dbConnections.Redshift.checkConnection(payload["params"])
        elif connectionName == "Snowflake":
            connectionResponse = dbConnections.Snowflake.checkConnection(payload["params"])
        elif connectionName == "Druid":
            connectionResponse = dbConnections.Druid.checkConnection(payload["params"])
        elif connectionName == "MySQL":
            connectionResponse = dbConnections.MySQL.checkConnection(payload["params"])
        elif connectionName == "Postgres":
            connectionResponse = dbConnections.Postgres.checkConnection(payload["params"])
        elif connectionName == "MSSQL":
            connectionResponse = dbConnections.MSSQL.checkConnection(payload["params"])
        elif connectionName == "ClickHouse":
            connectionResponse = dbConnections.ClickHouse.checkConnection(payload["params"])
        else:
            connectionResponse = True

        if connectionResponse:
            connection = Connection.objects.create(
                name=payload["name"],
                description=payload["description"],
                connectionType=connectionType,
            )

            for param in payload["params"]:
                cp = ConnectionParam.objects.get(
                    name=param, connectionType=connectionType
                )
                ConnectionParamValue.objects.create(
                    connectionParam=cp,
                    value=payload["params"][param],
                    connection=connection,
                )

            res.update(True, "Connection added successfully")
        else:
            logger.error("DB connection failed :")
            res.update(False, "Connection Failed")

        return res

    @staticmethod
    def removeConnection(connection_id):
        """
        Remove connection of given connection_id
        """
        res = ApiResponse("Erorr in deleting connection")
        connection = Connection.objects.filter(id=connection_id)
        if len(connection) > 0:
            Connection.objects.get(id=connection_id).delete()
            res.update(True, "Connection deleted successfully")
        else:
            res.update(
                False, "Cannot delete connection because it is linked with datasets"
            )
        return res

    @staticmethod
    def updateConnection(connection_id, payload):
        """
        Update connection of giben connection_id

        """
        res = ApiResponse("Error in updating connection")
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
        """
        Gets available connection types
        """
        res = ApiResponse("Error in fetching connection types")
        connectionTypes = ConnectionType.objects.all()
        data = ConnectionTypeSerializer(connectionTypes, many=True).data
        res.update(True, "Successfully retrieved connection types", data)
        return res
