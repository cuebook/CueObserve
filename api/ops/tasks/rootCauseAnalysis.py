import json
import traceback
import datetime as dt
import pandas as pd
import html2text
from django.template import Template, Context
from celery import shared_task, group
from celery.result import allow_join_result

from anomaly.models import Anomaly, RootCauseAnalysis, RCAAnomaly

from anomaly.serializers import AnomalySerializer
from access.data import Data
from access.utils import prepareAnomalyDataframes

# ANOMALY_DAILY_TEMPLATE = "Anomaly Daily Template"
# ANOMALY_HOURLY_TEMPLATE = "Anomaly Hourly Template"

RCA_RUNNING = "RUNNING"
RCA_SUCCESS = "SUCCESS"
RCA_ERROR = "ERROR"


@shared_task
def _anomalyDetectionForValue(anomalyId: int, dimension: str, dimVal: str, contriPercent: float, dfDict: list):
    """
    Internal anomaly detection subtask to be grouped by celery for each anomaly object
    """
    from anomaly.services import RootCauseAnalyses

    anomalyServiceResult = RootCauseAnalyses.createRCAAnomaly(
        anomalyId, dimension, dimVal, contriPercent, pd.DataFrame(dfDict)
    )
    return anomalyServiceResult


@shared_task
def _anomalyDetectionForDimension(anomalyId: int, dimension: str, data: list):
    """
    Method to find initiate anomaly detection for a given anomaly definition
    :param dimension: 
    :para 
    """

    anomaly = Anomaly.objects.get(id=anomalyId)
    try:
        df = pd.DataFrame(data=data)
        dimValsData = prepareAnomalyDataframes(
            df,
            anomaly.anomalyDefinition.dataset.timestampColumn,
            anomaly.anomalyDefinition.metric,
            dimension,
            10,
        )


        # detectionJobs = group(
        #     _anomalyDetectionForValue.s(
        #         anomalyId,
        #         dimension,
        #         obj["dimVal"],
        #         obj["contriPercent"],
        #         obj["df"].to_dict("records"),
        #     )
        #     for obj in dimValsData
        # )
        # _detectionJobs = detectionJobs.apply_async()
        # with allow_join_result():
        #     result = _detectionJobs.get()

        [ _anomalyDetectionForValue(
                anomalyId,
                dimension,
                obj["dimVal"],
                obj["contriPercent"],
                obj["df"].to_dict("records"),
            )
            for obj in dimValsData ]
        # Anomaly.objects.filter(
        #     id__in=[anomaly["anomalyId"] for anomaly in result if anomaly["success"]]
        # ).update(latestRun=runStatusObj)
        # logs["numAnomaliesPulished"] = len(
        #     [anomaly for anomaly in result if anomaly.get("published")]
        # )
        # logs["numAnomalySubtasks"] = len(_detectionJobs)
        # logs["log"] = json.dumps(
        #     {detection.id: detection.result for detection in _detectionJobs}
        # )
        # allTasksSucceeded = all([anomalyTask["success"] for anomalyTask in result])
    except Exception as ex:
        # logs["log"] = json.dumps(
        #     {"stackTrace": traceback.format_exc(), "message": str(ex)}
        # )
        # runStatusObj.status = ANOMALY_DETECTION_ERROR
        pass
    # else:
    #     runStatusObj.status = ANOMALY_DETECTION_SUCCESS
    # if not allTasksSucceeded:
    #     runStatusObj.status = ANOMALY_DETECTION_ERROR
    # runStatusObj.logs = logs
    # runStatusObj.endTimestamp = dt.datetime.now()
    # runStatusObj.save()


@shared_task
def rootCauseAnalysisJob(anomalyId: int):
    """
    Method to do root cause analysis for a given anomaly
    :param anomaly_id: Id of anomaly.anomaly model's object
    """

    from anomaly.services.slack import SlackAlert

    anomaly = Anomaly.objects.get(id=anomalyId)
    # Todo remove already existing rca data
    # Todo fetch related data
    logs = {}
    try:
        datasetDf = Data.fetchDatasetDataframe(anomaly.anomalyDefinition.dataset)

        dimension = anomaly.anomalyDefinition.dimension
        dimensions = json.loads(anomaly.anomalyDefinition.dataset.dimensions)
        otherDimensions = [x for x in dimensions if x != dimension]

        filteredDf = datasetDf[datasetDf[dimension] == anomaly.dimensionVal]
        timestampColumn = anomaly.anomalyDefinition.dataset.timestampColumn
        metric = anomaly.anomalyDefinition.metric

        results = [
            _anomalyDetectionForDimension(
                anomalyId, dim, filteredDf[[timestampColumn, metric, dim]].to_dict("records")
            )
            for dim in otherDimensions
        ]



        # detectionJobs = group(
        #     _anomalyDetectionForDimension.s(
        #         anomalyDef_id,
        #         obj["dimVal"],
        #         obj["contriPercent"],
        #         obj["df"].to_dict("records"),
        #     )
        #     for obj in dimValsData
        # )
        # _detectionJobs = detectionJobs.apply_async()
        # with allow_join_result():
        #     result = _detectionJobs.get()

        # logs["numAnomaliesPulished"] = len(
        #     [anomaly for anomaly in result if anomaly.get("published")]
        # )
        # logs["numAnomalySubtasks"] = len(_detectionJobs)
        # logs["log"] = json.dumps(
        #     {detection.id: detection.result for detection in _detectionJobs}
        # )
        # allTasksSucceeded = all([anomalyTask["success"] for anomalyTask in result])

        "We'll get the measure & filter from there\
        Get all other dimesion other than that \
        & for each get top values & parallely run AD and store in redis"
        rootCauseAnalysis, _ = RootCauseAnalysis.objects.get_or_create(anomaly=anomaly )
        rootCauseAnalysis.status=RCA_RUNNING
        rootCauseAnalysis.save()

    except Exception as ex:
        logs["log"] = json.dumps(
            {"stackTrace": traceback.format_exc(), "message": str(ex)}
        )
        rootCauseAnalysis.status = RCA_ERROR
    else:
        rootCauseAnalysis.status = RCA_SUCCESS
    # if not allTasksSucceeded:
    #     rootCauseAnalysis.status = RCA_ERROR
    rootCauseAnalysis.logs = logs
    rootCauseAnalysis.endTimestamp = dt.datetime.now()
    rootCauseAnalysis.save()
