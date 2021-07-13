import os
import datetime as dt
import pandas as pd
from celery import shared_task, group
from celery.result import allow_join_result

from anomaly.models import AnomalyDefinition
from access.data import Data
from access.utils import prepareAnomalyDataframes
from ops.anomalyDetection import anomalyService


@shared_task
def _anomalyDetectionSubTask(anomalyDef_id, dimVal, contriPercent, dfDict):
    """
    Internal anomaly detection subtask to be grouped by celery for each anomaly object
    """
    anomalyDefinition = AnomalyDefinition.objects.get(id=anomalyDef_id)
    anomalyProcess = anomalyService(anomalyDefinition, dimVal, contriPercent, pd.DataFrame(dfDict))


@shared_task
def anomalyDetectionJob(anomalyDef_id: int):
    """
    Method to find initiate anomaly detection for a given anomaly definition
    :param anomalyDef_id: ID of the anomaly definition
    """
    anomalyDefinition = AnomalyDefinition.objects.get(id=anomalyDef_id)
    datasetDf = Data.fetchDatasetDataframe(anomalyDefinition.dataset)
    dimValsData = prepareAnomalyDataframes(datasetDf, anomalyDefinition.dataset.timestampColumn, anomalyDefinition.metric, anomalyDefinition.dimension, anomalyDefinition.top)
    # for obj in dimValsData:
    #     _anomalyDetectionSubTask(anomalyDef_id, obj["dimVal"], obj["contriPercent"], obj["df"].to_dict("records"))
    detectionJobs = group(
        _anomalyDetectionSubTask.s(anomalyDef_id, obj["dimVal"], obj["contriPercent"], obj["df"].to_dict("records")) for obj in dimValsData
    )
    _detectionJobs = detectionJobs.apply_async()
    with allow_join_result():
        result = _detectionJobs.get()
