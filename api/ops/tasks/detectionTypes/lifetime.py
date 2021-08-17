import dateutil.parser as dp
from dateutil.relativedelta import relativedelta
import pandas as pd, datetime as dt


def checkLatestAnomaly(df):
    """
    Looks up latest anomaly in dataframe
    """
    anomalies = df[df["anomaly"] == 15]
    if anomalies.shape[0] > 0:
        lastAnomalyRow = anomalies.iloc[-1]
        anomalyTime = lastAnomalyRow["ds"]

        return {
            "highOrLow": "high" if lastAnomalyRow["y"] == df.y.max() else "low",
            "value": float(lastAnomalyRow["y"]),
            "anomalyTimeISO": dp.parse(anomalyTime).isoformat(),
            "anomalyTime": dp.parse(anomalyTime).timestamp() * 1000,
        }
    return {}

def lifetimeDetect(df, granularity):
    """
    Method to perform anomaly detection on given dataframe
    """
    today = dt.datetime.now()
    df["ds"] = pd.to_datetime(df["ds"])
    df = df.sort_values("ds")
    df["ds"] = df["ds"].apply(lambda date: date.isoformat()[:19])
    todayISO = today.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat()[:19]
    df = df[df["ds"] < todayISO]
    maxVal = df.y.max()
    minVal = df.y.min()
    df["anomaly"] = ((df["y"] == maxVal) | (df["y"] == minVal)) * 14 + 1
    anomalyLatest = checkLatestAnomaly(df)
    df = df[["ds", "y", "anomaly"]]
    numActual = 45 if granularity == "day" else 24 * 7
    output = {
        "anomalyData": {
            "actual": df[-numActual:].to_dict("records")
        },
        "anomalyLatest": anomalyLatest
    }
    return output