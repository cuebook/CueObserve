import json
import traceback
import datetime as dt
import pandas as pd
from celery import shared_task, group
from celery.result import allow_join_result

from anomaly.models import Anomaly, AnomalyDefinition, RunStatus
from access.data import Data
from access.utils import prepareAnomalyDataframes
from ops.anomalyDetection import anomalyService
from anomaly.services.slack import SlackAlert

ANOMALY_DETECTION_RUNNING = "RUNNING"
ANOMALY_DETECTION_SUCCESS = "SUCCESS"
ANOMALY_DETECTION_ERROR = "ERROR"

@shared_task
def _anomalyDetectionSubTask(anomalyDef_id, dimVal, contriPercent, dfDict):
    """
    Internal anomaly detection subtask to be grouped by celery for each anomaly object
    """
    anomalyDefinition = AnomalyDefinition.objects.get(id=anomalyDef_id)
    anomalyServiceResult = anomalyService(anomalyDefinition, dimVal, contriPercent, pd.DataFrame(dfDict))
    return anomalyServiceResult


@shared_task
def anomalyDetectionJob(anomalyDef_id: int, manualRun: bool = False):
    """
    Method to find initiate anomaly detection for a given anomaly definition
    :param anomalyDef_id: ID of the anomaly definition
    :param manualRun: Boolean determining whether task was manually initiated
    """
    runType = "Manual" if manualRun else "Scheduled"
    anomalyDefinition = AnomalyDefinition.objects.get(id=anomalyDef_id)
    anomalyDefinition.anomaly_set.update(published=False)
    runStatusObj = RunStatus.objects.create(anomalyDefinition=anomalyDefinition, status=ANOMALY_DETECTION_RUNNING, runType=runType)
    logs = {}
    allTasksSucceeded = False
    try:
        datasetDf = Data.fetchDatasetDataframe(anomalyDefinition.dataset)
        dimValsData = prepareAnomalyDataframes(datasetDf, anomalyDefinition.dataset.timestampColumn, anomalyDefinition.metric, anomalyDefinition.dimension, anomalyDefinition.top)
        detectionJobs = group(
            _anomalyDetectionSubTask.s(anomalyDef_id, obj["dimVal"], obj["contriPercent"], obj["df"].to_dict("records")) for obj in dimValsData
        )
        _detectionJobs = detectionJobs.apply_async()
        with allow_join_result():
            result = _detectionJobs.get()
        Anomaly.objects.filter(id__in=[anomaly["anomalyId"] for anomaly in result if anomaly["success"]]).update(latestRun=runStatusObj)
        logs["numAnomaliesPulished"] = len([anomaly for anomaly in result if anomaly.get("published")])
        logs["numAnomalySubtasks"] = len(_detectionJobs)
        logs["log"] = json.dumps({detection.id: detection.result for detection in _detectionJobs})
        allTasksSucceeded = all([anomalyTask["success"] for anomalyTask in result])
    except Exception as ex:
        logs["log"] = json.dumps({"stackTrace": traceback.format_exc(), "message": str(ex)})
        runStatusObj.status = ANOMALY_DETECTION_ERROR
    else:
        runStatusObj.status = ANOMALY_DETECTION_SUCCESS
    if not allTasksSucceeded:
        runStatusObj.status = ANOMALY_DETECTION_ERROR
    runStatusObj.logs = logs
    runStatusObj.endTimestamp = dt.datetime.now()
    runStatusObj.save()

    # Slack alerts
    title = "CueObserve Alerts"
    if runStatusObj.status == ANOMALY_DETECTION_SUCCESS:
        message = "Anomaly Detection Job succeeded for AnomalyDefintion id : " + str(anomalyDef_id) + "\n"
        message = message + "Numer of anomaly subtasks: " + str(logs["numAnomalySubtasks"]) + "\n"
        message = message + "Numer of anomalies published: " + str(logs["numAnomaliesPulished"]) + "\n"
        resultsLog = json.loads(logs["log"])
        if len(resultsLog.values()) > 1:
            message = message + "Dimension Values:" + "\n"
            for subtask in resultsLog.values():
                pub = "Published" if subtask["published"] else "Not Published"
                message = message + "  " + subtask["dimVal"] + ": " + pub + "\n"
        name = "anomalyAlert"
        SlackAlert.slackAlertHelper(title, message, name)
    
    if runStatusObj.status == ANOMALY_DETECTION_ERROR:
        message = "Anomaly Detection Job failed on AnomalyDefintion id : " + str(anomalyDef_id) + "\n"
        message = message + str(logs["log"])
        name = "appAlert"
        SlackAlert.slackAlertHelper(title, message, name)