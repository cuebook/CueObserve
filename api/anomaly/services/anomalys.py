import json
from django.template import Template, Context
from utils.apiResponse import ApiResponse
from anomaly.models import Dataset, Anomaly, AnomalyCardTemplate
from anomaly.serializers import DatasetsSerializer, DatasetSerializer, AnomalySerializer


class Anomalys:
    """
    Class to deal with functionalities related to anomaly model
    """

    @staticmethod
    def getAnomalys():
        """
        Gets anomalys
        """
        res = ApiResponse("Error in getting anomalies")
        # data = [
        #     {
        #         "id": 5,
        #         "title": "Card title",
        #         "text": "Card text",
        #         "dimVal": "Delhi",
        #         "filterContribution": 34,
        #         "data": {
        #             "chartData": [],
        #         },
        #         "lastAnomalyTimeISO": "20190403",
        #     }
        # ]
        anomalies = Anomaly.objects.all()
        data = AnomalySerializer(anomalies, many=True).data
        res.update(True, "Successfully retrieved anomalies", data)
        return res

    @staticmethod
    def getAnomaly(anomalyId: int):
        """
        Gets anomaly
        :param anomalyId: id of anomaly to fetch
        """
        res = ApiResponse("Error in getting specified anomaly")
        anomalyObj = Anomaly.objects.get(id=anomalyId)

        data = AnomalySerializer(anomalyObj).data

        cardTemplate = AnomalyCardTemplate.objects.get(templateName="Anomaly Daily Template")

        data["title"] = Template(cardTemplate.title).render(Context(data))
        data["text"] = Template(cardTemplate.bodyText).render(Context(data))

        res.update(True, "Successfully retrieved specified anomaly", data)
        return res
