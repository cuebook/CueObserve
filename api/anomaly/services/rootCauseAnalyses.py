import json
import traceback
import datetime as dt
import dateutil.parser as dp
from utils.apiResponse import ApiResponse


from anomaly.models import RootCauseAnalysis, RCAAnomaly, Anomaly
from ops.anomalyDetection import detect, dataFrameEmpty


class RootCauseAnalyses:
    """
    Class to deal with functionalities associataed with RCA
    """

    @staticmethod
    def calculateRCA(anomalyId: int):
        """
        Trigger calculate RCA job
        """
        res = ApiResponse("Error in triggering RCA calculation")
        res.update(True, "Successfully triggered RCA calculation")
        return res

    @staticmethod
    def getRCA(anomalyId: int):
        """
        Get data for RCA
        :param anomalyId:
        """
        res = ApiResponse("Error in getting RCA")
        anomaly = Anomaly.objects.get(id=anomalyId)

        rcaAnomalies = RCAAnomaly.objects.filter(anomaly_id=anomalyId)
        data = {
            "anomalyContribution": anomaly.data["contribution"],
            "rcaAnomalies": list(rcaAnomalies.values()),
        }

        res.update(True, "Successfully retrieved RCA", data)
        return res

    @staticmethod
    def createRCAAnomaly(
        anomalyId: int, dimension: str, dimensionValue: str, contriPercent: float, df
    ):
        """ """
        anomaly = Anomaly.objects.get(id=anomalyId)
        output = {"dimVal": dimensionValue, "success": True}
        toPublish = False
        try:
            if dataFrameEmpty(df):
                return
            granularity = anomaly.anomalyDefinition.dataset.granularity
            result = detect(df, granularity)

            del result["anomalyData"]["predicted"]
            # removing anomalous point other than last one
            anomalyTimeISO = anomaly.data["anomalyLatest"]["anomalyTimeISO"]
            for row in result["anomalyData"]["actual"]:
                if row["ds"] == anomalyTimeISO and row["anomaly"] == 15:
                    toPublish = True
                    result["value"] = row["y"]
                else:
                    row["anomaly"] = 1

            # removing prediction band
            result["anomalyData"]["band"] = result["anomalyData"]["band"][:-15]

            result["contribution"] = contriPercent
            result["anomalyLatest"]["contribution"] = contriPercent
            timeThreshold = 3600 * 24 * 5 if granularity == "day" else 3600 * 24
            # toPublish = (
            #     dt.datetime.now().timestamp()
            #     - dp.parse(result["anomalyLatest"]["anomalyTimeISO"]).timestamp()
            #     <= timeThreshold
            # )
            # if anomalyDef.highOrLow:
            #     toPublish = (
            #         toPublish
            #         and anomalyDef.highOrLow.lower()
            #         == result["anomalyLatest"]["highOrLow"]
            #     )
        except Exception as ex:
            output["error"] = json.dumps(
                {"message": str(ex), "stackTrace": traceback.format_exc()}
            )
            output["success"] = False
        if toPublish:
            rcaAnomaly, _ = RCAAnomaly.objects.get_or_create(
                anomaly_id=anomalyId, dimension=dimension, dimensionValue=dimensionValue
            )
            rcaAnomaly.data = result
            rcaAnomaly.save()
            output["rcaAnomalyId"] = rcaAnomaly.id

        return output
