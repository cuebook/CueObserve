from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from anomaly.services import Anomalys, Datasets


class AnomalysView(APIView):
    """ """

    def get(self, request):
        """ """
        res = Anomalys.getAnomalys()
        return Response(res.json())


class DatasetsView(APIView):
    """
    Provides views on datasets(many)
    """

    def get(self, request):
        """get request"""
        res = Datasets.getDatasets()
        return Response(res.json())


class DatasetView(APIView):
    """
    Provided views on Dataset(single)
    """

    def get(self, request, datasetId: int):
        """get request"""
        res = Datasets.getDataset(datasetId)
        return Response(res.json())

    def post(self, request, datasetId: int):
        """post request"""
        data = request.data
        res = Datasets.updateDataset(datasetId, data)
        return Response(res.json())

    def delete(self, request, datasetId: int):
        """delete request"""
        res = Datasets.deleteDataset(datasetId)
        return Response(res.json())


class CreateDatasetView(APIView):
    """
    Provides view on creating Dataset
    """

    def post(self, request):
        """post request"""
        data = request.data
        res = Datasets.createDataset(data)
        return Response(res.json())
