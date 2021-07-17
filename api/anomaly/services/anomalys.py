from django.template import Template, Context
from utils.apiResponse import ApiResponse
from anomaly.models import Anomaly, AnomalyCardTemplate
from anomaly.serializers import AnomalySerializer

ANOMALY_DAILY_TEMPLATE = "Anomaly Daily Template"
ANOMALY_HOURLY_TEMPLATE= "Anomaly Hourly Template"

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
        anomalies = Anomaly.objects.filter(published=True)
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

        templateName = ANOMALY_DAILY_TEMPLATE if anomalyObj.anomalyDefinition.dataset.granularity == "day" else ANOMALY_HOURLY_TEMPLATE
        cardTemplate = AnomalyCardTemplate.objects.get(templateName=templateName)
        data.update(data["data"]["anomalyLatest"])

        data["title"] = Template(cardTemplate.title).render(Context(data))
        data["text"] = Template(cardTemplate.bodyText).render(Context(data))

        res.update(True, "Successfully retrieved specified anomaly", data)
        return res
