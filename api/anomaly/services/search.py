import os
import json
import logging
import requests
from utils.apiResponse import ApiResponse
from anomaly.models import Dataset
from anomaly.services import Datasets
from anomaly.serializers import AllDimensionsSerializer, AllMeticsSerializer
from access.data import Data

class SearchUtils:
    """ Provides service related to search """
    def getAllDimensions():
        """ Gets dimension from all datasets """
        res = ApiResponse()
        datasets = Dataset.objects.all() # Get all datasets
        data = AllDimensionsSerializer(datasets, many=True).data
        res.update(True,"Successfully data transfer",data)
        return res

    def getAllMetrics():
        """ Gets metric from all datasets """
        res = ApiResponse()
        logging.info("get metrics from cueobserve")
        datasets = Dataset.objects.all() # Get all datasets
        data = AllMeticsSerializer(datasets, many=True).data
        res.update(True, "Successfully data transfer between CueObserve and Search services", data)
        return res

    def getDimValues(payload):
        res = ApiResponse()
        try:
            datasetId = int(payload.get("datasetId"))
            dimension = payload.get("dimension",'')
            dataset = Dataset.objects.get(id=datasetId)
            df = Data.fetchDatasetDataframe(dataset)
            data = df[dimension].to_list()[:30]
            res.update(True, "Successfully data transfer between CueObserve and Search services", data)
            return res
        except Exception as ex:
            logging.error("DatasetId OR dimension does not exists %s", ex)
            res.update(False, "No dimension values found", [])
            return res
