import os
import datetime as dt
import pandas as pd
from celery import shared_task, group
from celery.result import allow_join_result

from anomaly.models import AnomalyDefinition, RunStatus
from access.data import Data
from access.utils import prepareAnomalyDataframes
from ops.anomalyDetection import anomalyService

ANOMALY_DETECTION_RUNNING = "RUNNING"
ANOMALY_DETECTION_SUCCESS = "SUCCESS"
ANOMALY_DETECTION_ERROR = "ERROR"

@shared_task
def _anomalyDetectionSubTask(anomalyDef_id, dimVal, contriPercent, dfDict):
    """
    Internal anomaly detection subtask to be grouped by celery for each anomaly object
    """
    anomalyDefinition = AnomalyDefinition.objects.get(id=anomalyDef_id)
    anomalyProcess = anomalyService(anomalyDefinition, dimVal, contriPercent, pd.DataFrame(dfDict))


@shared_task
def anomalyDetectionJob(anomalyDef_id: int, manualRun: bool = False):
    """
    Method to find initiate anomaly detection for a given anomaly definition
    :param anomalyDef_id: ID of the anomaly definition
    :param manualRun: Boolean determining whether task was manually initiated
    """
    runType = "Manual" if manualRun else "Scheduled"
    anomalyDefinition = AnomalyDefinition.objects.get(id=anomalyDef_id)
    runStatusObj = RunStatus.objects.create(anomalyDefinition=anomalyDefinition, status=ANOMALY_DETECTION_RUNNING, runType=runType)
    try:
        datasetDf = Data.fetchDatasetDataframe(anomalyDefinition.dataset)
        dimValsData = prepareAnomalyDataframes(datasetDf, anomalyDefinition.dataset.timestampColumn, anomalyDefinition.metric, anomalyDefinition.dimension, anomalyDefinition.top)
        detectionJobs = group(
            _anomalyDetectionSubTask.s(anomalyDef_id, obj["dimVal"], obj["contriPercent"], obj["df"].to_dict("records")) for obj in dimValsData
        )
        _detectionJobs = detectionJobs.apply_async()
        with allow_join_result():
            result = _detectionJobs.get()
    except:
        runStatusObj.status = ANOMALY_DETECTION_ERROR
    else:
        runStatusObj.status = ANOMALY_DETECTION_SUCCESS
    runStatusObj.endTimestamp = dt.datetime.now()
    runStatusObj.save()
