import json
import dateutil.parser as dp
import datetime as dt
from rest_framework import serializers
from anomaly.models import Anomaly, Dataset, Connection, ConnectionType, AnomalyDefinition, CustomSchedule as Schedule


class ConnectionSerializer(serializers.ModelSerializer):
    connectionTypeId = serializers.SerializerMethodField()
    connectionType = serializers.SerializerMethodField()
    datasetCount = serializers.SerializerMethodField()


    def get_connectionTypeId(self, obj):
        return obj.connectionType.id

    def get_connectionType(self, obj):
        return obj.connectionType.name

    def get_datasetCount(self, obj):
        connectionId = obj.id
        datasetCount = Dataset.objects.filter(connection_id = connectionId).count()
        return datasetCount

    class Meta:
        model = Connection
        fields = [
            "id",
            "name",
            "description",
            "connectionTypeId",
            "connectionType",
            "datasetCount"
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
        fields = ['id', 'name', 'granularity', 'connection', 'anomalyDefinitionCount']


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
    datasetName = serializers.SerializerMethodField()
    granularity = serializers.SerializerMethodField()
    metric = serializers.SerializerMethodField()
    dimension = serializers.SerializerMethodField()
    anomalyTimeStr = serializers.SerializerMethodField()

    def get_datasetName(self, obj):
        return obj.anomalyDefinition.dataset.name

    def get_granularity(self, obj):
        return obj.anomalyDefinition.dataset.granularity

    def get_metric(self, obj):
        return obj.anomalyDefinition.metric

    def get_dimension(self, obj):
        return obj.anomalyDefinition.dimension

    def get_anomalyTimeStr(self, obj):
        anomalyTs = dp.parse(obj.data["anomalyLatest"]["anomalyTimeISO"])
        gran = obj.anomalyDefinition.dataset.granularity
        if gran == "day":
            delta = (dt.datetime.now() - anomalyTs).days
            if delta <= 1:
                return "Yesterday"
            return f"{delta} days ago"
        elif gran == "hour":
            delta = int((dt.datetime.now() - anomalyTs).total_seconds() / 3600)
            return f"{delta} hours ago"

    class Meta:
        model = Anomaly
        fields = ["id", "datasetName", "published", "dimension", "dimensionVal", "granularity", "metric", "anomalyTimeStr", "data"]

class ScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the model CrontabSchedule
    """
    schedule = serializers.SerializerMethodField()
    crontab = serializers.SerializerMethodField()
    timezone = serializers.SerializerMethodField()
    def get_schedule(self, obj):
        """
        Gets string form of the crontab
        """
        return str(obj.cronSchedule)

    def get_timezone(self, obj):
        """ Gets schedule timezone"""
        return str(obj.cronSchedule.timezone)

    def cronexp(self, field):
        return field and str(field).replace(' ', '') or '*'
    
    def get_crontab(self, obj):
        """Gets schedule crontab """
        return '{0} {1} {2} {3} {4}'.format(
            self.cronexp(obj.cronSchedule.minute), self.cronexp(obj.cronSchedule.hour),
            self.cronexp(obj.cronSchedule.day_of_month), self.cronexp(obj.cronSchedule.month_of_year),
            self.cronexp(obj.cronSchedule.day_of_week)
        )

    class Meta:
        model = Schedule
        fields = ["id", "schedule","name","timezone","crontab"]
