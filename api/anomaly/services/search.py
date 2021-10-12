import os
import json
import logging
import requests
from utils.apiResponse import ApiResponse
from anomaly.models import Dataset
from anomaly.services import Datasets
from anomaly.serializers import AllDimensionsSerializer, AllMeticsSerializer
ENVIRONMENT_URL = os.environ.get("ENVIRONMENT_URL", "http://localhost:8200")
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
