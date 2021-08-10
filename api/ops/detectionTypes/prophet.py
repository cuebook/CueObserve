import dateutil.parser as dp
from dateutil.relativedelta import relativedelta
import pandas as pd, datetime as dt
from prophet import Prophet


def isAnomaly(lowBand, highBand, value):
    """Condition for anomaly on a certain row"""
    if value < lowBand or value > highBand:
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
        higher = lastAnomalyRow["y"] > lastAnomalyRow["upper"]

        per = 0
        denom = lastAnomalyRow["upper"] if higher else lastAnomalyRow["lower"]
        if denom > 0:
            per = int(100 * (abs(lastAnomalyRow["y"] - denom) / denom))

        return {
            "highOrLow": "high" if higher else "low",
            "value": float(lastAnomalyRow["y"]),
            "percent": per,
            "anomalyTimeISO": dp.parse(anomalyTime).isoformat(),
            "anomalyTime": dp.parse(anomalyTime).timestamp() * 1000,
        }

def prophetDetect(df, granularity):
    """
    Method to perform anomaly detection on given dataframe using fbProphet
    """
    today = dt.datetime.now()
    df["ds"] = pd.to_datetime(df["ds"])
    df["ds"] = df["ds"].apply(lambda date: date.isoformat()[:19])
    todayISO = today.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).isoformat()[:19]
    df = df[df["ds"] < todayISO]
    lastActualRow = df[-1:]
    lastISO = df.iloc[-1]["ds"]
    if granularity == "hour":
        lastWeekISO = (dp.parse(lastISO) + relativedelta(days=-7)).isoformat()
        df = df[df["ds"] > lastWeekISO]
    prophetModel = Prophet(
        changepoint_prior_scale=0.01,
        seasonality_prior_scale=1.0,
        interval_width=0.75
    )
    prophetModel.fit(df)
    numPredictions = 15 if granularity == "day" else 24
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
    numActual = 45 if granularity == "day" else 24 * 7
    output = {
        "anomalyData": {
            "actual": df[-numActual:].to_dict("records"),
            "predicted": forecast.to_dict("records"),
            "band": band[-(numActual + numPredictions):].to_dict("records"),
        },
        "anomalyLatest": anomalyLatest
    }
    return output