import json
import traceback
import datetime as dt
import pandas as pd
from anomaly.services.alerts import EmailAlert
import html2text
from django.template import Template, Context
from celery import shared_task, group
from celery.result import allow_join_result

from anomaly.models import (
    Anomaly,
    AnomalyDefinition,
    RunStatus,
    AnomalyCardTemplate,
    RCAAnomaly,
)
from anomaly.serializers import AnomalySerializer
from access.data import Data
from access.utils import prepareAnomalyDataframes

from .anomalyDetection import anomalyService

ANOMALY_DETECTION_RUNNING = "RUNNING"
ANOMALY_DETECTION_SUCCESS = "SUCCESS"
ANOMALY_DETECTION_ERROR = "ERROR"


@shared_task
def _anomalyDetectionSubTask(anomalyDef_id, dimVal, contriPercent, dfDict):
    """
    Internal anomaly detection subtask to be grouped by celery for each anomaly object
    """
    anomalyDefinition = AnomalyDefinition.objects.get(id=anomalyDef_id)
    anomalyServiceResult = anomalyService(
        anomalyDefinition, dimVal, contriPercent, pd.DataFrame(dfDict)
    )
    return anomalyServiceResult


@shared_task
def anomalyDetectionJob(anomalyDef_id: int, manualRun: bool = False):
    """
    Method to find initiate anomaly detection for a given anomaly definition
    :param anomalyDef_id: ID of the anomaly definition
    :param manualRun: Boolean determining whether task was manually initiated
    """

    from anomaly.services.alerts import SlackAlert

    runType = "Manual" if manualRun else "Scheduled"
    anomalyDefinition = AnomalyDefinition.objects.get(id=anomalyDef_id)
    anomalyDefinition.anomaly_set.update(published=False)
    RCAAnomaly.objects.filter(anomaly__in=anomalyDefinition.anomaly_set.all()).delete()

    runStatusObj = RunStatus.objects.create(
        anomalyDefinition=anomalyDefinition,
        status=ANOMALY_DETECTION_RUNNING,
        runType=runType,
    )
    logs = {}
    allTasksSucceeded = False
    try:
        datasetDf = Data.fetchDatasetDataframe(anomalyDefinition.dataset)
        dimValsData = prepareAnomalyDataframes(
            datasetDf,
            anomalyDefinition.dataset.timestampColumn,
            anomalyDefinition.metric,
            anomalyDefinition.dimension,
            anomalyDefinition.operation,
            float(anomalyDefinition.value),
        )

        detectionJobs = group(
            _anomalyDetectionSubTask.s(
                anomalyDef_id,
                obj["dimVal"],
                obj["contriPercent"],
                obj["df"].to_dict("records"),
            )
            for obj in dimValsData
        )
        _detectionJobs = detectionJobs.apply_async()
        with allow_join_result():
            result = _detectionJobs.get()

        Anomaly.objects.filter(
            id__in=[anomaly["anomalyId"] for anomaly in result if anomaly["success"]]
        ).update(latestRun=runStatusObj)

        logs["numAnomaliesPulished"] = len(
            [anomaly for anomaly in result if anomaly.get("published")]
        )
        logs["numAnomalySubtasks"] = len(_detectionJobs)
        logs["log"] = json.dumps(
            {detection.id: detection.result for detection in _detectionJobs}
        )
        allTasksSucceeded = all([anomalyTask["success"] for anomalyTask in result])
    except Exception as ex:
        logs["log"] = json.dumps(
            {"stackTrace": traceback.format_exc(), "message": str(ex)}
        )
        runStatusObj.status = ANOMALY_DETECTION_ERROR
    else:
        runStatusObj.status = ANOMALY_DETECTION_SUCCESS
    if not allTasksSucceeded:
        runStatusObj.status = ANOMALY_DETECTION_ERROR
    runStatusObj.logs = logs
    runStatusObj.endTimestamp = dt.datetime.now()
    runStatusObj.save()

    ################################################# Slack Alert ########################################################
    title = "CueObserve Alerts"
    if runStatusObj.status == ANOMALY_DETECTION_SUCCESS:
        if logs.get("numAnomaliesPulished", 0) > 0:
            numPublished = logs["numAnomaliesPulished"]
            message = f"{numPublished} {'anomalies' if numPublished > 1 else 'anomaly'} published. \n"
            topNtext = (
                f" Top {anomalyDefinition.value}"
                if int(float(anomalyDefinition.value)) > 0
                else ""
            )
            dimText = f" {anomalyDefinition.dimension}" if anomalyDefinition.dimension else ""
            highLowText = f" {anomalyDefinition.highOrLow}" if anomalyDefinition.highOrLow else ""
            message = (
                message
                + f"Anomaly Definition: *{anomalyDefinition.metric}{dimText}{highLowText}{topNtext}* \n"
            )
            message = (
                message
                + f"Dataset: {anomalyDefinition.dataset.name} | Granularity: {anomalyDefinition.dataset.granularity} \n \n"
            )
            highestContriAnomaly = anomalyDefinition.anomaly_set.order_by(
                "data__contribution"
            ).last()
            anomalyId = highestContriAnomaly.id
            data = AnomalySerializer(highestContriAnomaly).data
            templateName = anomalyDefinition.getAnomalyTemplateName()
            cardTemplate = AnomalyCardTemplate.objects.get(templateName=templateName)
            data.update(data["data"]["anomalyLatest"])

            details = (
                html2text.html2text(Template(cardTemplate.title).render(Context(data))).replace("**", "*")
                + "\n"
            )
            details = details + html2text.html2text(
                Template(cardTemplate.bodyText).render(Context(data))
            )

            name = "anomalyAlert"
            SlackAlert.slackAlertHelper(title, message, name, details=details, anomalyId=anomalyId)
        
            ################################################## Email Alert ############################################################

            numPublished = logs["numAnomaliesPulished"]
            messageHtml = f"{numPublished} {'anomalies' if numPublished > 1 else 'anomaly'} published. <br>"
            messageHtml = (
                messageHtml
                + f"Anomaly Definition: <b>{anomalyDefinition.metric}{dimText}{highLowText}{topNtext}</b> <br>"
            )
            messageHtml = (
                messageHtml
                + f"Dataset: {anomalyDefinition.dataset.name} <br>"
            )
            messageHtml = (
                messageHtml +  f"Granularity: {anomalyDefinition.dataset.granularity} <br> <br>"
            )
            emailSubject = (
                html2text.html2text(Template(cardTemplate.title).render(Context(data))).replace("**", "").replace("\n","")
            
            )
            detailsHtml = Template(cardTemplate.title).render(Context(data)) + "<br>"
            subjectHtml = emailSubject
           
            detailsHtml = detailsHtml + Template(cardTemplate.bodyText).render(Context(data)) +"<br>"
            EmailAlert.sendEmail(messageHtml, detailsHtml, subjectHtml, anomalyId)

    if runStatusObj.status == ANOMALY_DETECTION_ERROR:
        message = (
            "Anomaly Detection Job failed on AnomalyDefintion id : "
            + str(anomalyDef_id)
            + "\n"
        )
        message = message + str(logs["log"])
        name = "appAlert"
        SlackAlert.slackAlertHelper(title, message, name)
