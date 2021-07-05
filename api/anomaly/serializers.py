import json
from rest_framework import serializers
from anomaly.models import Anomaly, Dataset, Connection, ConnectionType, AnomalyDefinition


class ConnectionSerializer(serializers.ModelSerializer):
    connectionTypeId = serializers.SerializerMethodField()
    connectionType = serializers.SerializerMethodField()

    def get_connectionTypeId(self, obj):
        return obj.connectionType.id

    def get_connectionType(self, obj):
        return obj.connectionType.name

    class Meta:
        model = Connection
        fields = [
            "id",
            "name",
            "description",
            "connectionTypeId",
            "connectionType",
        ]


class ConnectionDetailSerializer(serializers.ModelSerializer):
    params = serializers.SerializerMethodField()
    connectionTypeId = serializers.SerializerMethodField()
    connectionType = serializers.SerializerMethodField()

    def get_params(self, obj):
        params = {}
        for val in obj.cpvc.all():
            params[val.connectionParam.name] = val.value if not val.connectionParam.isEncrypted else "**********"
        return params

    def get_connectionTypeId(self, obj):
        return obj.connectionType.id

    def get_connectionType(self, obj):
        return obj.connectionType.name

    class Meta:
        model = Connection
        fields = [
            "id",
            "name",
            "description",
            "params",
            "connectionTypeId",
            "connectionType",
        ]


class ConnectionTypeSerializer(serializers.ModelSerializer):
    
    params = serializers.SerializerMethodField()

    def get_params(self, obj):
        paramList = []
        for param in obj.connectionTypeParam.all():
            params = {}
            params["id"] = param.id
            params["name"] = param.name
            params["label"] = param.label
            params["isEncrypted"] = param.isEncrypted
            params["properties"] = param.properties
            paramList.append(params)
        return paramList

    class Meta:
        model = ConnectionType
        fields = ["id", "name", "params"]


class DatasetsSerializer(serializers.ModelSerializer):
    """
    Serializes data related to anomaly tree 
    """
    connection = ConnectionSerializer()
    anomalyDefinitionCount = serializers.SerializerMethodField()

    def get_anomalyDefinitionCount(self, obj):
        """
        Gets anomaly definition count
        """
        return obj.anomalydefinition_set.count()

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'connection', 'anomalyDefinitionCount']


class DatasetSerializer(serializers.ModelSerializer):
    """
    Serializes data related to anomaly tree 
    """
    connection = ConnectionSerializer()
    dimensions = serializers.SerializerMethodField()
    metrics = serializers.SerializerMethodField()
    anomalyDefinitionCount = serializers.SerializerMethodField()

    def get_anomalyDefinitionCount(self, obj):
        """
        Gets anomaly definition count
        """
        return obj.anomalydefinition_set.count()

    def get_dimensions(self, obj):
        dimensions = json.loads(obj.dimensions) if obj.metrics else []
        return dimensions if dimensions else []

    def get_metrics(self, obj):
        metrics = json.loads(obj.metrics) if obj.metrics else []
        return metrics if metrics else []

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'sql', 'connection', 'dimensions', 'metrics', 'granularity', 'timestampColumn', 'anomalyDefinitionCount']

class AnomalyDefinitionSerializer(serializers.ModelSerializer):
    """
    Serializes data related to anomlay Definition
    """
    dataset = DatasetSerializer()
    anomalyDef = serializers.SerializerMethodField()
    def get_anomalyDef(self, obj):
        params = {}
        params["id"] = obj.id
        params["metric"] = obj.metric
        params["dimension"] = obj.dimension
        params["highOrLow"] = obj.highOrLow
        params["top"] = obj.top
        return params
    
    class Meta:
        model = AnomalyDefinition
        fields = ["id",  "anomalyDef", "dataset"]

class AnomalySerializer(serializers.ModelSerializer):
    """
    Serializes data for anomaly
    """
    anomalyDefinition = AnomalyDefinitionSerializer()

    class Meta:
        model = Anomaly
        fields = ["id", "anomalyDefinition", "published", "dimensionVal", "data"]