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
def _anomalyDetectionSubTask(anomalyDef_id, dimVal, dfDict):
    """
    Internal anomaly detection subtask to be grouped by celery for each anomaly object
    """
    anomalyDefinition = AnomalyDefinition.objects.get(id=anomalyDef_id)
    anomalyProcess = anomalyService(anomalyDefinition, dimVal, pd.DataFrame(dfDict))


@shared_task
def anomalyDetectionJob(anomalyDef_id: int):
    """
    Method to find initiate anomaly detection for a given anomaly definition
    :param anomalyDef_id: ID of the anomaly definition
    """
    anomalyDefinition = AnomalyDefinition.objects.get(id=anomalyDef_id)
    datasetDf = Data.fetchDatasetDataframe(anomalyDefinition.dataset)
    dimVals, dataframes = prepareAnomalyDataframes(datasetDf, anomalyDefinition.dataset.timestampColumn, anomalyDefinition.metric, anomalyDefinition.dimension, anomalyDefinition.top)
    for i in range(len(dimVals)):
        _anomalyDetectionSubTask(anomalyDef_id, dimVals[i], dataframes[i].to_dict("records"))
    # detectionJobs = group(
    #     _anomalyDetectionSubTask.s(anomalyDef_id, dimVals[i], dataframes[i].to_dict("records")) for i in range(len(dimVals))
    # )
    # _detectionJobs = detectionJobs.apply_async()
    # with allow_join_result():
    #     result = _detectionJobs.get()
