import dateutil.parser as dp
from dateutil.relativedelta import relativedelta
import pandas as pd, datetime as dt


def checkLatestAnomaly(df, operationCheckStr):
    """
    Looks up latest anomaly in dataframe
    """
    anomalies = df[df["anomaly"] == 15]
    if anomalies.shape[0] > 0:
        lastAnomalyRow = anomalies.iloc[-1]
        anomalyTime = lastAnomalyRow["ds"]

        return {
            "operationCheck": operationCheckStr,
            "value": float(lastAnomalyRow["y"]),
            "anomalyTimeISO": dp.parse(anomalyTime).isoformat(),
            "anomalyTime": dp.parse(anomalyTime).timestamp() * 1000,
        }
    return {}

def valueThresholdDetect(df, granularity, operator, value1, value2):
    """
    Method to perform anomaly detection on given dataframe
    """
    value1 = int(value1)
    lowerVal = value1
    upperVal = value1
    if value2 != "null":
        value2 = int(value2)
        lowerVal = min(value1, value2)
        upperVal = max(value1, value2)
    
    operationStrDict = {
        "greater": f'greater than {value1}',
        "lesser": f'lesser than {value1}',
        "!greater": f'not greater than {value1}',
        "!lesser": f'not lesser than {value1}',
        "between": f'between {lowerVal} and {upperVal}',
        "!between": f'not between {lowerVal} and {upperVal}'
    }

    operationDict = {
        "greater": '(df["y"] > value1) * 14 + 1',
        "lesser": '(df["y"] < value1) * 14 + 1',
        "!greater": '(df["y"] <= value1) * 14 + 1',
        "!lesser": '(df["y"] >= value1) * 14 + 1',
        "between": '((df["y"] >= lowerVal) & (df["y"] <= upperVal)) * 14 + 1',
        "!between": '((df["y"] < lowerVal) | (df["y"] > upperVal)) * 14 + 1'
    }
    today = dt.datetime.now()
    df["ds"] = pd.to_datetime(df["ds"])
    df = df.sort_values("ds")
    df["ds"] = df["ds"].apply(lambda date: date.isoformat()[:19])
    todayISO = today.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat()[:19] if granularity == "day" else today.replace(minute=0, second=0, microsecond=0, tzinfo=None).isoformat()[:19]
    df = df[df["ds"] < todayISO]
    df["anomaly"] = eval(operationDict[operator])
    anomalyLatest = checkLatestAnomaly(df, operationStrDict[operator])
    df = df[["ds", "y", "anomaly"]]
    numActual = 45 if granularity == "day" else 24 * 7
    output = {
        "anomalyData": {
            "actual": df[-numActual:].to_dict("records")
        },
        "anomalyLatest": anomalyLatest
    }
    return output