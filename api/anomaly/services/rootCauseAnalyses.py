import json
import traceback
import datetime as dt
import dateutil.parser as dp

from anomaly.models import RootCauseAnalysis, RCAAnomaly, Anomaly
from ops.anomalyDetection import detect, dataFrameEmpty


class RootCauseAnalyses:
    """
    Class to deal with functionalities associataed with RCA
    """

    @staticmethod
    def createRCAAnomaly(anomalyId: int, dimension:str, dimensionValue: str, contriPercent: float, df):
        """
        """
        anomaly = Anomaly.objects.get(id=anomalyId)
        output = {"dimVal": dimensionValue, "success": True}
        toPublish = False
        try: 
            if dataFrameEmpty(df):
                return
            granularity = anomaly.anomalyDefinition.dataset.granularity
            result = detect(df, granularity)
            result['contribution'] = contriPercent
            result["anomalyLatest"]["contribution"] = contriPercent
            timeThreshold = 3600 * 24 * 5 if granularity == "day" else 3600 * 24
            toPublish = (
                dt.datetime.now().timestamp()
                - dp.parse(result["anomalyLatest"]["anomalyTimeISO"]).timestamp()
                <= timeThreshold
            )
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

        rcaAnomaly, _ = RCAAnomaly.objects.get_or_create(
                anomaly_id=anomalyId, dimension=dimension, dimensionValue=dimensionValue
            )
        rcaAnomaly.data = result
        rcaAnomaly.save()
        output["rcaAnomalyId"] = rcaAnomaly.id

        return output

