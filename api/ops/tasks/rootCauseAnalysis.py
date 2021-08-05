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


@shared_task
def _anomalyDetectionForDimension(anomalyId: int, dimension: str, data: list):
    """
    Method to find initiate anomaly detection for a given anomaly definition
    :param anomaly_id: id of anomaly object under analysis
    :param dimension: dimension for which anomaly is being detected
    :para data: data for dimension
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

        anomaly.rootcauseanalysis.logs = {
            **anomaly.rootcauseanalysis.logs,
            dimension: "Ananlyzing..",
        }
        anomaly.rootcauseanalysis.save()

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
        _detectionJobs = detectionJobs.apply_async()
        with allow_join_result():
            results = _detectionJobs.get()

        anomaly = Anomaly.objects.get(id=anomalyId)
        anomaly.rootcauseanalysis.logs = {
            **anomaly.rootcauseanalysis.logs,
            dimension: "Analyzed",
        }
        anomaly.rootcauseanalysis.save()

        if not all(results):
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

    from anomaly.services.slack import SlackAlert

    anomaly = Anomaly.objects.get(id=anomalyId)
    rootCauseAnalysis, _ = RootCauseAnalysis.objects.get_or_create(anomaly=anomaly)
    rootCauseAnalysis.startTimestamp = dt.datetime.now()
    rootCauseAnalysis.endTimestamp = None
    rootCauseAnalysis.logs = {}
    rootCauseAnalysis.status = RootCauseAnalysis.STATUS_RUNNING
    rootCauseAnalysis.save()

    # Remove already existing rca data
    anomaly.rcaanomaly_set.all().delete()

    # Todo fetch related data
    try:
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

        rootCauseAnalysis.logs = {
            **rootCauseAnalysis.logs,
            "Analyzing Dimensions": ", ".join(otherDimensions),
        }
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
        rootCauseAnalysis.logs = {
            **rootCauseAnalysis.logs,
            "Error Stack Trace": traceback.format_exc(),
            "Error Message": str(ex),
        }
        rootCauseAnalysis.status = RootCauseAnalysis.STATUS_ERROR
    rootCauseAnalysis.endTimestamp = dt.datetime.now()
    rootCauseAnalysis.save()
