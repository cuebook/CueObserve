import json
from utils.apiResponse import ApiResponse
from anomaly.models import Dataset
from anomaly.serializers import DatasetsSerializer, DatasetSerializer


class Anomalys:
    """
    Class to deal with functionalities related to anomaly model
    """

    @staticmethod
    def getAnomalys():
        """
        Gets anomalys
        """
        res = ApiResponse("Error in getting datasets")
        # datasets = Dataset.objects.all()
        # data = DatasetsSerializer(datasets, many=True).data
        data = [
            {
                "id": 5,
                "title": "Card title",
                "text": "Card text",
                "dimVal": "Delhi",
                "filterContribution": 34,
                "data": {
                    "chartData": [],
                },
                "lastAnomalyTimeISO": "20190403",
            }
        ]
        res.update(True, "Successfully retrieved datasets", data)
        return res

    @staticmethod
    def getAnomaly(anomalyId: int):
        """
        Gets anomaly
        :param anomalyId: id of anomaly to fetch
        """
        res = ApiResponse("Error in getting datasets")

        data = None

        res.update(True, "Successfully retrieved datasets", data)
        return res
