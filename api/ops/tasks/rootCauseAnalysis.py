import json
import time
import logging
import traceback
import datetime as dt
import pandas as pd
import html2text
from django.template import Template, Context
from celery import shared_task, group
from celery.result import allow_join_result
from app.celery import app

from anomaly.models import Anomaly, RootCauseAnalysis, RCAAnomaly

from anomaly.serializers import AnomalySerializer
from access.data import Data
from access.utils import prepareAnomalyDataframes
from anomaly.services.telemetry import rca_event_log

# ANOMALY_DAILY_TEMPLATE = "Anomaly Daily Template"
# ANOMALY_HOURLY_TEMPLATE = "Anomaly Hourly Template"
logger = logging.getLogger(__name__)


@shared_task
def _anomalyDetectionForValue(
    anomalyId: int,
    dimension: str,
    dimensionVal: str,
    contriPercent: float,
    dfDict: list,
):
    """
    Internal anomaly detection subtask to be grouped by celery for each anomaly object
    :param anomaly_id: id of anomaly object under analysis
    :param dimension: dimension for which anomaly is being detected
    :param dimensionVal: dimension value being analyzed
    :para data: data for dimension
    """

    from anomaly.services import RootCauseAnalyses

    try:
        anomalyServiceResult = RootCauseAnalyses.createRCAAnomaly(
            anomalyId, dimension, dimensionVal, contriPercent, pd.DataFrame(dfDict)
        )
        return anomalyServiceResult
    except Exception as ex:
        return False


def _parallelizeAnomalyDetection(anomalyId: int, dimension: str, dimValsData: list):
    """
    Run anomaly detection in parallel in celery
    :param dimValsData: Data for anomaly detection
    """
    detectionJobs = group(
        _anomalyDetectionForValue.s(
            anomalyId,
            dimension,
            obj["dimVal"],
            obj["contriPercent"],
            obj["df"].to_dict("records"),
        )
        for obj in dimValsData
    )

    rootCauseAnalysis = RootCauseAnalysis.objects.get(anomaly_id=anomalyId)
    _detectionJobs = detectionJobs.apply_async()

    taskIds = [task.id for task in _detectionJobs.children]
    rootCauseAnalysis.taskIds = [*rootCauseAnalysis.taskIds, *taskIds]
    rootCauseAnalysis.save()

    with allow_join_result():
        results = _detectionJobs.get()
    return results


@shared_task
def _anomalyDetectionForDimension(anomalyId: int, dimension: str, data: list):
    """
    Method to find initiate anomaly detection for a given anomaly definition
    :param anomaly_id: id of anomaly object under analysis
    :param dimension: dimension for which anomaly is being detected
    :para data: data for dimension
    """
    DEFAULT_OPERATION = "Min % Contribution"
    DEFAULT_OPERATION_VALUE = 1

    anomaly = Anomaly.objects.get(id=anomalyId)
    try:
        df = pd.DataFrame(data=data)

        operation = anomaly.anomalyDefinition.operation
        operationValue = int(anomaly.anomalyDefinition.value)
        operationValue = operationValue if operation else DEFAULT_OPERATION_VALUE
        operation = operation if operation else DEFAULT_OPERATION

        dimValsData = prepareAnomalyDataframes(
            df,
            anomaly.anomalyDefinition.dataset.timestampColumn,
            anomaly.anomalyDefinition.metric,
            dimension,
            operation,
            operationValue,
        )

        anomaly.rootcauseanalysis.logs = {
            **anomaly.rootcauseanalysis.logs,
            dimension: "Analyzing..",
        }
        anomaly.rootcauseanalysis.save()

        results = _parallelizeAnomalyDetection(anomalyId, dimension, dimValsData)

        anomaly = Anomaly.objects.get(id=anomalyId)
        anomaly.rootcauseanalysis.logs = {
            **anomaly.rootcauseanalysis.logs,
            dimension: "Analyzed",
        }
        anomaly.rootcauseanalysis.save()

        if not all([x["success"] for x in results]):
            return False
    except Exception as ex:

        anomaly.rootcauseanalysis.logs = {
            **anomaly.rootcauseanalysis.logs,
            dimension: "Analysis Failed",
            dimension + " Error Stack Trace": traceback.format_exc(),
            dimension + " Error Message": str(ex),
        }
        anomaly.rootcauseanalysis.save()
        return False

    return True


@shared_task
def rootCauseAnalysisJob(anomalyId: int):
    """
    Method to do root cause analysis for a given anomaly
    :param anomaly_id: id of anomaly object under analysis
    """

    from anomaly.services.alerts import SlackAlert

    anomaly = Anomaly.objects.get(id=anomalyId)
    rootCauseAnalysis, _ = RootCauseAnalysis.objects.get_or_create(anomaly=anomaly)
    rootCauseAnalysis.startTimestamp = dt.datetime.now()
    rootCauseAnalysis.endTimestamp = None
    rootCauseAnalysis.logs = {}
    rootCauseAnalysis.status = RootCauseAnalysis.STATUS_RUNNING
    rootCauseAnalysis.taskIds = [
        *rootCauseAnalysis.taskIds,
        rootCauseAnalysisJob.request.id,
    ]
    rootCauseAnalysis.save()

    logger.info("Removing already existing rca data")
    anomaly.rcaanomaly_set.all().delete()

    # Todo pre-fetch related data
    try:
        # **rootCauseAnalysis.logs,
        rootCauseAnalysis = RootCauseAnalysis.objects.get(anomaly=anomaly)
        rootCauseAnalysis.logs = {"Data": "Fetching..."}
        rootCauseAnalysis.save()
        datasetDf = Data.fetchDatasetDataframe(anomaly.anomalyDefinition.dataset)

        dimension = anomaly.anomalyDefinition.dimension
        dimensions = json.loads(anomaly.anomalyDefinition.dataset.dimensions)
        otherDimensions = [x for x in dimensions if x != dimension]

        if dimension:
            filteredDf = datasetDf[datasetDf[dimension] == anomaly.dimensionVal]
        else:
            filteredDf = datasetDf
        timestampColumn = anomaly.anomalyDefinition.dataset.timestampColumn
        metric = anomaly.anomalyDefinition.metric
        rootCauseAnalysis = RootCauseAnalysis.objects.get(anomaly=anomaly)
        # **rootCauseAnalysis.logs,
        # "Data": "Fetched",
        rootCauseAnalysis.logs = {"Analyzing Dimensions": ", ".join(otherDimensions)}
        rootCauseAnalysis.save()
        results = [
            _anomalyDetectionForDimension(
                anomalyId,
                dim,
                filteredDf[[timestampColumn, metric, dim]].to_dict("records"),
            )
            for dim in otherDimensions
        ]

        rootCauseAnalysis = RootCauseAnalysis.objects.get(anomaly=anomaly)
        if all(results):
            rootCauseAnalysis.status = RootCauseAnalysis.STATUS_SUCCESS
        else:
            rootCauseAnalysis.status = RootCauseAnalysis.STATUS_ERROR
    except Exception as ex:
        rootCauseAnalysis = RootCauseAnalysis.objects.get(anomaly=anomaly)
        rootCauseAnalysis.logs = {
            **rootCauseAnalysis.logs,
            "Error Stack Trace": traceback.format_exc(),
            "Error Message": str(ex),
        }
        rootCauseAnalysis.status = RootCauseAnalysis.STATUS_ERROR
    rootCauseAnalysis.endTimestamp = dt.datetime.now()
    rootCauseAnalysis.save()
    rca_event_log(rootCauseAnalysis.status)
    return True
