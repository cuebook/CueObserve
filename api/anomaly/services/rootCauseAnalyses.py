import json
import logging
import traceback
import datetime as dt
import dateutil.parser as dp
from utils.apiResponse import ApiResponse
from ops.tasks import rootCauseAnalysisJob
from app.celery import app

from anomaly.models import RootCauseAnalysis, RCAAnomaly, Anomaly
from anomaly.serializers import RootCauseAnalysisSerializer, RCAAnomalySerializer
from ops.tasks.anomalyDetection import detect, dataFrameEmpty

logger = logging.getLogger(__name__)


class RootCauseAnalyses:
    """
    Class to deal with functionalities associataed with RCA
    """

    @staticmethod
    def calculateRCA(anomalyId: int):
        """
        Trigger job for RCA calculation
        :param anomalyId: id of anomaly object needed to be analyzed
        """
        res = ApiResponse("Error in triggering RCA calculation")
        rootCauseAnalysis, _ = RootCauseAnalysis.objects.get_or_create(
            anomaly_id=anomalyId
        )
        rootCauseAnalysis.status = RootCauseAnalysis.STATUS_RECEIVED
        rootCauseAnalysis.save()
        task = rootCauseAnalysisJob.delay(anomalyId)
        rootCauseAnalysis = RootCauseAnalysis.objects.get(anomaly_id=anomalyId)
        rootCauseAnalysis.taskIds = [*rootCauseAnalysis.taskIds, task.id]
        rootCauseAnalysis.save()

        res.update(True, "Successfully triggered RCA calculation")
        return res

    @staticmethod
    def getRCA(anomalyId: int):
        """
        Get data for RCA
        :param anomalyId: id of anomaly object whose RCA to be fetched
        """
        res = ApiResponse("Error in getting RCA")
        anomaly = Anomaly.objects.get(id=anomalyId)

        rcaAnomalies = RCAAnomaly.objects.filter(anomaly_id=anomalyId).order_by(
            "-data__anomalyLatest__value"
        )
        rcaAnomaliesData = RCAAnomalySerializer(rcaAnomalies, many=True).data
        data = {
            "status": None,
            "logs": None,
            "startTimestamp": None,
            "endTimestamp": None,
        }
        if hasattr(anomaly, "rootcauseanalysis"):
            data = {
                **data,
                **RootCauseAnalysisSerializer(anomaly.rootcauseanalysis).data,
            }

        data = {
            **data,
            "granularity": anomaly.anomalyDefinition.dataset.granularity,
            "measure": anomaly.anomalyDefinition.metric,
            "dimension": anomaly.anomalyDefinition.dimension,
            "dimensionValue": anomaly.dimensionVal,
            "value": anomaly.data["anomalyLatest"]["value"],
            "anomalyContribution": anomaly.data["contribution"],
            "rcaAnomalies": rcaAnomaliesData,
            "anomalyTime": anomaly.data["anomalyLatest"]["anomalyTimeISO"],
        }

        res.update(True, "Successfully retrieved RCA", data)
        return res

    @staticmethod
    def abortRCA(anomalyId: int):
        """
        Abort RCA
        :param anomalyId: id of anomaly object whose RCA needs to be aborted
        """
        res = ApiResponse("Error in aborting RCA")
        try:
            rootCauseAnalysis = RootCauseAnalysis.objects.get(anomaly_id=anomalyId)
            app.control.revoke(rootCauseAnalysis.taskIds, terminate=True)

            rootCauseAnalysis.status = RootCauseAnalysis.STATUS_ABORTED
            rootCauseAnalysis.endTimestamp = dt.datetime.now()
            rootCauseAnalysis.save()
            res.update(True, "Successfully triggered RCA calculation")

        except Exception as ex:
            logger.error("Error in aborting RCA:%s", str(ex))

        return res

    @staticmethod
    def createRCAAnomaly(
        anomalyId: int, dimension: str, dimensionValue: str, contriPercent: float, df
    ):
        """
        Create RCA Anomaly for given anomalyId, dimension, dimensionValue
        :param anomalyId: id of anomaly object being analyzed
        :param dimension: dimension for which anomaly is being analyzed
        :param dimensionValue: dimension value for which anomaly is being analyzed
        :param contriPercent: percent contribution of given dimension: dimensionValue is whole
        :param df: data for anomaly detection
        """
        anomaly = Anomaly.objects.get(id=anomalyId)
        output = {"dimVal": dimensionValue, "success": True}
        try:
            if dataFrameEmpty(df):
                return output
            granularity = anomaly.anomalyDefinition.dataset.granularity
            result = detect(
                df, granularity, "Prophet", anomaly.anomalyDefinition, limit=6
            )

            del result["anomalyData"]["predicted"]
            # removing anomalous point other than last one
            anomalyTimeISO = anomaly.data["anomalyLatest"]["anomalyTimeISO"]
            if (
                not "anomalyLatest" in result
                or not result["anomalyLatest"]
                or result["anomalyLatest"]["anomalyTimeISO"] != anomalyTimeISO
            ):
                return output

            for row in result["anomalyData"]["actual"]:
                if not (row["ds"] == anomalyTimeISO and row["anomaly"] == 15):
                    row["anomaly"] = 1
                else:
                    row["anomaly"] = 6

            # removing prediction band
            result["anomalyData"]["band"] = result["anomalyData"]["band"][:-15]

            result["contribution"] = contriPercent
            result["anomalyLatest"]["contribution"] = contriPercent

            rcaAnomaly, _ = RCAAnomaly.objects.get_or_create(
                anomaly_id=anomalyId, dimension=dimension, dimensionValue=dimensionValue
            )
            rcaAnomaly.data = result
            rcaAnomaly.save()
            output["rcaAnomalyId"] = rcaAnomaly.id

        except Exception as ex:
            output["error"] = json.dumps(
                {"message": str(ex), "stackTrace": traceback.format_exc()}
            )
            output["success"] = False

        return output
