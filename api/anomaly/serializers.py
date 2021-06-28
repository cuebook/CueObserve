from rest_framework import serializers
from anomaly.models import Dataset

class DatasetsSerializer(serializers.ModelSerializer):
    """
    Serializes data related to anomaly tree 
    """

    class Meta:
        model = Dataset
        fields = ['id', 'name']


class DatasetSerializer(serializers.ModelSerializer):
    """
    Serializes data related to anomaly tree 
    """

    class Meta:
        model = Dataset
        fields = ['id', 'name', 'sql']

