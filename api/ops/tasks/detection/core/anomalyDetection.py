import json
import traceback
import datetime as dt
import dateutil.parser as dp

import pandas as pd

from .detectionTypes.prophet import prophetDetect
from .detectionTypes.percentageChange import percentChangeDetect
from .detectionTypes.lifetime import lifetimeDetect
from .detectionTypes.valueThreshold import valueThresholdDetect

def dataFrameEmpty(df):
    """Checks whether dataFrame has enough data for prophet"""
    if df is None:
        return True
    if df.empty:
        return True
    if df.shape[0] < 20:
        return True
    return False


def detect(df, granularity, detectionRuleType, detectionParams, limit=None):
    """
    Method to detect anomaly depending on the detection rule type
    """
    if detectionRuleType == "Prophet":
        return prophetDetect(df, granularity, limit)
    elif detectionRuleType == "Percentage Change":
        return percentChangeDetect(df, granularity, detectionParams["threshold"])
    elif detectionRuleType == "Lifetime High/Low":
        return lifetimeDetect(df, granularity)
    elif detectionRuleType == "Value Threshold":
        return valueThresholdDetect(df, granularity, detectionParams["operator"], detectionParams["value1"], detectionParams["value2"])


def anomalyService(dimValObj, dfDict, anomalyDefProps, detectionRuleType, detectionParams):
    """
    Method to conduct the anomaly detection process
    """
    df = pd.DataFrame(dfDict)
    anomalyId = dimValObj["anomalyId"]
    dimVal = dimValObj["dimVal"]
    contriPercent = dimValObj["contriPercent"]
    output = {"dimVal": dimVal, "anomalyId": anomalyId}
    granularity = anomalyDefProps["granularity"]
    try:
        if dataFrameEmpty(df):
            output["error"] = json.dumps({"message": "Insufficient data in dataframe."})
            output["success"] = False
            return output

        result = detect(df, granularity, detectionRuleType, detectionParams)
        result["contribution"] = contriPercent
        toPublish = False
        if result["anomalyLatest"]:
            result["anomalyLatest"]["contribution"] = contriPercent
            timeThreshold = 3600 * 24 * 5 if granularity == "day" else 3600 * 24
            toPublish = (
                dt.datetime.now().timestamp()
                - dp.parse(result["anomalyLatest"]["anomalyTimeISO"]).timestamp()
                <= timeThreshold
            )
            if anomalyDefProps["highOrLow"]:
                toPublish = (
                    toPublish
                    and anomalyDefProps["highOrLow"].lower()
                    == result["anomalyLatest"]["highOrLow"]
                )
        output["data"] = result
        output["published"] = toPublish
        output["success"] = True
    except Exception as ex:
        output["error"] = json.dumps(
            {"message": str(ex), "stackTrace": traceback.format_exc()}
        )
        output["success"] = False

    return output
