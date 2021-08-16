import traceback
import dateutil.parser as dp
import pandas as pd, datetime as dt, json

from .detectionTypes.prophet import prophetDetect
from .detectionTypes.percentageChange import percentChangeDetect
from .detectionTypes.lifetime import lifetimeDetect
from .detectionTypes.valueThreshold import valueThresholdDetect

from anomaly.models import Anomaly


def dataFrameEmpty(df):
    """Checks whether dataFrame has enough data for prophet"""
    if df is None:
        return True
    if df.empty:
        return True
    if df.shape[0] < 20:
        return True
    return False


def detect(df, granularity, detectionRuleType, anomalyDef):
    """
    Method to detect anomaly depending on the detection rule type
    """
    if detectionRuleType == "Prophet":
        return prophetDetect(df, granularity)
    elif detectionRuleType == "Percentage Change":
        threshold = float(anomalyDef.detectionrule.detectionruleparamvalue_set.get(param__name="threshold").value)
        return percentChangeDetect(df, granularity, threshold)
    elif detectionRuleType == "Lifetime":
        return lifetimeDetect(df, granularity)
    elif detectionRuleType == "Value Threshold":
        lowerThreshold = anomalyDef.detectionrule.detectionruleparamvalue_set.get(param__name="lowerThreshold").value
        upperThreshold = anomalyDef.detectionrule.detectionruleparamvalue_set.get(param__name="upperThreshold").value
        return valueThresholdDetect(df, granularity, lowerThreshold, upperThreshold)



def anomalyService(anomalyDef, dimVal, contriPercent, df):
    """
    Method to conduct the anomaly detection process
    """
    anomalyObj, _ = Anomaly.objects.get_or_create(anomalyDefinition=anomalyDef, dimensionVal=dimVal, published=False)
    output = {"dimVal": dimVal}
    try:
        if dataFrameEmpty(df):
            output["error"] = json.dumps({"message": "Insufficient data in dataframe."})
            output["success"] = False
            return output
        granularity = anomalyDef.dataset.granularity
        detectionRuleType = anomalyDef.detectionrule.detectionRuleType.name if hasattr(anomalyDef, "detectionrule") else "Prophet"
        result = detect(df, granularity, detectionRuleType, anomalyDef)
        result["contribution"] = contriPercent
        toPublish= False
        if result["anomalyLatest"]:
            result["anomalyLatest"]["contribution"] = contriPercent
            timeThreshold = 3600 * 24 * 5 if granularity == "day" else 3600 * 24
            toPublish = dt.datetime.now().timestamp() - dp.parse(result["anomalyLatest"]["anomalyTimeISO"]).timestamp() <= timeThreshold
            if anomalyDef.highOrLow:
                toPublish = toPublish and anomalyDef.highOrLow.lower() == result["anomalyLatest"]["highOrLow"]
        anomalyObj.data = result
        anomalyObj.published = toPublish
        anomalyObj.save()
        output["published"] = toPublish
        output["anomalyId"] = anomalyObj.id
        output["success"] = True
    except Exception as ex:
        output["error"] = json.dumps({"message": str(ex), "stackTrace": traceback.format_exc()})
        output["success"] = False

    
    return output



    
    



