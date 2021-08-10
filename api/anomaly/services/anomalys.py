import json
import traceback
import datetime as dt
import dateutil.parser as dp
from django.template import Template, Context
from utils.apiResponse import ApiResponse
from django.db.models import Q
from anomaly.models import Anomaly, AnomalyCardTemplate
from anomaly.serializers import AnomalySerializer

from ops.anomalyDetection import detect, dataFrameEmpty



class Anomalys:
    """
    Class to deal with functionalities related to anomaly model
    """

    @staticmethod
    def getAnomalys(
        publishedOnly: bool = False,
        offset: int = 0,
        limit: int = 50,
        searchQuery: str = None,
        sorter: dict = {},
    ):
        """
        Gets anomalys
        """
        res = ApiResponse("Error in getting anomalies")
        anomaliesObj = (
            Anomaly.objects.filter(published=True)
            if publishedOnly
            else Anomaly.objects.all()
        )
        count = anomaliesObj.count()

        if searchQuery:
            anomaliesObj = Anomalys.__searchOnAnomalys(anomaliesObj, searchQuery)
            count = anomaliesObj.count()
        if sorter.get("order", False):
            anomaliesObj = Anomalys.sortOnAnomalys(anomaliesObj, sorter)
        anomaliesObj = anomaliesObj[offset : offset + limit]
        anomalies = AnomalySerializer(anomaliesObj, many=True).data
        data = {"anomalies": anomalies, "count": count}
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

        templateName = anomalyObj.anomalyDefinition.getAnomalyTemplateName()
        cardTemplate = AnomalyCardTemplate.objects.get(templateName=templateName)
        data.update(data["data"]["anomalyLatest"])

        data["title"] = Template(cardTemplate.title).render(Context(data))
        data["text"] = Template(cardTemplate.bodyText).render(Context(data))

        res.update(True, "Successfully retrieved specified anomaly", data)
        return res

    @staticmethod
    def __searchOnAnomalys(anomaliesObj, searchQuery: str):
        """
        Gets anomaly on user search
        :param anomaliesObj: Objects of model Anomaly.Anomaly
        :param searchQuery: string to be searched
        """

        return anomaliesObj.filter(
            Q(anomalyDefinition__metric__icontains=searchQuery)
            | Q(dimensionVal__icontains=searchQuery)
            | Q(anomalyDefinition__dataset__name__icontains=searchQuery)
            | Q(anomalyDefinition__dataset__granularity__icontains=searchQuery)
            | Q(anomalyDefinition__dimension__icontains=searchQuery)
        )

    @staticmethod
    def sortOnAnomalys(anomaliesObj, sorter):
        """
        Sort anomaly on user input
        """

        columnToSort = sorter.get("columnKey", "")
        sortOrder = sorter.get("order", "")

        if columnToSort == "datasetName" and sortOrder == "ascend":
            anomaliesObj = anomaliesObj.order_by("anomalyDefinition__dataset__name")
        if columnToSort == "datasetName" and sortOrder == "descend":
            anomaliesObj = anomaliesObj.order_by("-anomalyDefinition__dataset__name")

        if columnToSort == "granularity" and sortOrder == "ascend":
            anomaliesObj = anomaliesObj.order_by(
                "anomalyDefinition__dataset__granularity"
            )

        if columnToSort == "granularity" and sortOrder == "descend":
            anomaliesObj = anomaliesObj.order_by(
                "-anomalyDefinition__dataset__granularity"
            )

        if columnToSort == "metric" and sortOrder == "ascend":
            anomaliesObj = anomaliesObj.order_by("anomalyDefinition__metric")

        if columnToSort == "metric" and sortOrder == "descend":
            anomaliesObj = anomaliesObj.order_by("-anomalyDefinition__metric")

        if columnToSort == "dimensionVal" and sortOrder == "ascend":
            anomaliesObj = anomaliesObj.order_by("dimensionVal")

        if columnToSort == "dimensionVal" and sortOrder == "descend":
            anomaliesObj = anomaliesObj.order_by("-dimensionVal")

        if columnToSort == "contribution" and sortOrder == "ascend":
            anomaliesObj = anomaliesObj.order_by("data__contribution")

        if columnToSort == "contribution" and sortOrder == "descend":
            anomaliesObj = anomaliesObj.order_by("-data__contribution")

        if columnToSort == "contribution" and sortOrder == "ascend":
            anomaliesObj = anomaliesObj.order_by("data__contribution")

        if columnToSort == "contribution" and sortOrder == "descend":
            anomaliesObj = anomaliesObj.order_by("-data__contribution")

        if columnToSort == "anomaly" and sortOrder == "ascend":
            anomaliesObj = anomaliesObj.order_by("data__anomalyLatest__percent")

        if columnToSort == "anomaly" and sortOrder == "descend":
            anomaliesObj = anomaliesObj.order_by("-data__anomalyLatest__percent")

        if columnToSort == "anomalyTimeISO" and sortOrder == "ascend":
            anomaliesObj = anomaliesObj.order_by("-data__anomalyLatest__anomalyTime")

        if columnToSort == "anomalyTimeISO" and sortOrder == "descend":
            anomaliesObj = anomaliesObj.order_by("data__anomalyLatest__anomalyTime")

        return anomaliesObj

    @staticmethod
    def createAnomaly(anomalyDef, dimVal: str, contriPercent: float, df):
        """
        Method to conduct the anomaly detection process
        :param anomalyDef: object of model anomaly.anomalyDefinition
        :param dimVal: dimension value
        :param contriPercent: percentage contribution of given dimension values
        :param df: dataframe with atleast timestamp & metric
        :returns :
        """
        anomalyObj, _ = Anomaly.objects.get_or_create(
            anomalyDefinition=anomalyDef, dimensionVal=dimVal, published=False
        )

        output = {"dimVal": dimVal}
        try:
            if dataFrameEmpty(df):
                return
            granularity = anomalyDef.dataset.granularity
            result = detect(df, granularity)
            result["contribution"] = contriPercent
            result["anomalyLatest"]["contribution"] = contriPercent
            timeThreshold = 3600 * 24 * 5 if granularity == "day" else 3600 * 24
            toPublish = (
                dt.datetime.now().timestamp()
                - dp.parse(result["anomalyLatest"]["anomalyTimeISO"]).timestamp()
                <= timeThreshold
            )
            if anomalyDef.highOrLow:
                toPublish = (
                    toPublish
                    and anomalyDef.highOrLow.lower()
                    == result["anomalyLatest"]["highOrLow"]
                )
            anomalyObj.data = result
            anomalyObj.published = toPublish
            anomalyObj.save()
            output["published"] = toPublish
            output["anomalyId"] = anomalyObj.id
            output["success"] = True
        except Exception as ex:
            output["error"] = json.dumps(
                {"message": str(ex), "stackTrace": traceback.format_exc()}
            )
            output["success"] = False

        return output
