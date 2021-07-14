import dateutil.parser as dp
import pandas as pd, datetime as dt, json
from prophet import Prophet

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


def isAnomaly(lowBand, highBand, value):
    """Condition for anomaly on a certain row"""
    mid = (lowBand + highBand) / 2
    if value < lowBand or value > highBand:
        if mid == 0:
            return True
        if (abs(value - mid) / mid) > 0.2:
            return True
    return False

def checkLatestAnomaly(df):
    """
    Looks up latest anomaly in dataframe
    """
    anomalies = df[df["anomaly"] == 15]
    if anomalies.shape[0] > 0:
        lastAnomalyRow = anomalies.iloc[-1]
        anomalyTime = lastAnomalyRow["ds"]
        expected = (lastAnomalyRow["lower"] + lastAnomalyRow["upper"]) / 2
        higher = lastAnomalyRow["y"] > expected

        per = 0
        if expected > 0:
            per = (
                int(100 * (abs(lastAnomalyRow["y"] - expected) / expected))
            )

        return {
            "highOrLow": "high" if higher else "low",
            "value": float(lastAnomalyRow["y"]),
            "percent": per,
            "anomalyTimeISO": dp.parse(anomalyTime).isoformat(),
            "anomalyTime": dp.parse(anomalyTime).timestamp() * 1000,
        }

def detect(df, granularity):
    """
    Method to perform anomaly detection on given dataframe
    """
    today = dt.datetime.now()
    df["ds"] = pd.to_datetime(df["ds"])
    df["ds"] = df["ds"].apply(lambda date: date.isoformat()[:19])
    todayISO = today.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat()[:19]
    df = df[df["ds"] < todayISO]
    lastActualRow = df[-1:]
    lastISO = df.iloc[-1]["ds"]
    prophetModel = Prophet(
        changepoint_prior_scale=0.01,
        seasonality_prior_scale=1.0,
        uncertainty_samples=100,
    )
    prophetModel.fit(df)
    numPredictions = 15 if granularity == "day" else 4
    if granularity == "day":
        future = prophetModel.make_future_dataframe(periods=numPredictions)
    elif granularity == "hour":
        future = prophetModel.make_future_dataframe(periods=numPredictions, freq="H")
    forecast = prophetModel.predict(future)
    for col in ["yhat", "yhat_lower", "yhat_upper"]:
        forecast[col] = forecast[col].clip(lower=0.0)
    forecast = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]]
    forecast.columns = ["ds", "y", "lower", "upper"]
    forecast.ds = forecast.ds.apply(lambda x: x.isoformat()[:19])
    forecast.y = forecast.y.apply(lambda x: int(x))
    df = pd.merge(df, forecast[["ds", "lower", "upper"]], how="left")
    df["anomaly"] = df.apply(lambda row: 15 if isAnomaly(row.lower, row.upper, row.y) else 1, axis=1)
    anomalyLatest = checkLatestAnomaly(df)
    df = df[["ds", "y", "anomaly"]]
    forecast["band"] = forecast.apply(lambda x: [x["lower"], x["upper"]], axis=1)
    band = forecast[["ds", "band"]]
    band.columns = ["ds", "y"]
    forecast = forecast[forecast["ds"] > lastISO]
    forecast = forecast[["ds", "y"]]
    forecast = pd.concat([lastActualRow, forecast], ignore_index=True)
    output = {
        "anomalyData": {
            "actual": df[-(3 * numPredictions) :].to_dict("records"),
            "predicted": forecast.to_dict("records"),
            "band": band[-(4 * numPredictions) :].to_dict("records"),
        },
        "anomalyLatest": anomalyLatest
    }
    return output



def anomalyService(anomalyDef, dimVal, contriPercent, df):
    """
    Method to conduct the anomaly detection process
    """
    if dataFrameEmpty(df):
        return
    granularity = anomalyDef.dataset.granularity
    result = detect(df, granularity)
    result["contribution"] = contriPercent
    result["anomalyLatest"]["contribution"] = contriPercent
    anomalyObj, _ = Anomaly.objects.get_or_create(anomalyDefinition=anomalyDef, dimensionVal=dimVal)
    timeThreshold = 3600 * 24 * 5
    toPublish = dt.datetime.now().timestamp() - dp.parse(result["anomalyLatest"]["anomalyTimeISO"]).timestamp() <= timeThreshold
    if anomalyDef.highOrLow:
        toPublish = toPublish and anomalyDef.highOrLow.lower() == result["anomalyLatest"]["highOrLow"]
    anomalyObj.data = result
    anomalyObj.published = toPublish
    anomalyObj.save()



    
    



