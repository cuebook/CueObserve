import os
import json
import asyncio
import traceback
import logging
import datetime as dt
import aiohttp
import html2text
from django.template import Template, Context
from django.db import transaction
from celery import shared_task, group
from celery.result import allow_join_result

from anomaly.services.alerts import EmailAlert, WebHookAlert
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

from ops.tasks.detection.core.anomalyDetection import anomalyService
from anomaly.services.telemetry import event_logs

ANOMALY_DETECTION_RUNNING = "RUNNING"
ANOMALY_DETECTION_SUCCESS = "SUCCESS"
ANOMALY_DETECTION_ERROR = "ERROR"

logger = logging.getLogger(__name__)

@shared_task
def _anomalyDetectionSubTask(dimValObj, dfDict, anomalyDefProps, detectionRuleType, detectionParams):
    """
    Internal anomaly detection subtask to be grouped by celery for each anomaly object
    """
    anomalyServiceResult = anomalyService(
        dimValObj, dfDict, anomalyDefProps, detectionRuleType, detectionParams
    )
    return anomalyServiceResult

async def _sendLambdaRequest(session, lambdaUrl, anomalyServiceObj):
    """
    Async method to send anomaly detection request to lambda
    :param session: ClientSession instance for aiohttp
    :param lambdaUrl: AWS Lambda invocation endpoint
    :param anomalyServiceObject: Dict containing parameter data for anomaly service
    """
    resp = await session.post(lambdaUrl, data=json.dumps(anomalyServiceObj))
    print(f"Request sent for {anomalyServiceObj['dimValObj']['dimVal']}")
    responseData = await resp.json()
    if(responseData.get("message") == "Endpoint request timed out"):
        resp = await session.post(lambdaUrl, data=json.dumps(anomalyServiceObj))
        print(f"Retrying request for {anomalyServiceObj['dimValObj']['dimVal']}")
        responseData = await resp.json()
    return responseData

async def concurrentLambdaRequests(lambdaUrl, anomalyServiceObjects):
    """
    Async method to create and collect coroutines for all lambda requests
    :param lambdaUrl: AWS Lambda invocation endpoint
    :param anomalyServiceObjects: List of dicts containing parameter data for anomaly service
    """
    async with aiohttp.ClientSession() as session:
        result = await asyncio.gather(
            *(
                _sendLambdaRequest(session, lambdaUrl, obj)
                    for obj in anomalyServiceObjects
                )
            )
        return result


@transaction.atomic
def createAnomalyObjects(dimValsData, anomalyDefinition):
    """
    Function to create anomaly objects for dimension values for an anomaly definition
    :param anomalyResult: List of dicts, each corresponding to a dimension value
    :param anomalyDefinition: AnomalyDefinition object for which to create Anomaly objects
    """
    for obj in dimValsData:
        anomalyObj, _ = Anomaly.objects.get_or_create(
            anomalyDefinition=anomalyDefinition, dimensionVal=obj["dimVal"], published=False
        )
        obj["anomalyId"] = anomalyObj.id

@transaction.atomic
def saveAnomalyObjects(anomalyResult):
    """
    Function to save the outputs from anomaly detection into respective Anomaly objects
    :param anomalyResult: List of anomaly detection outputs
    """
    for obj in anomalyResult:
        anomalyObj = Anomaly.objects.get(id=obj["anomalyId"])
        anomalyObj.data = obj["data"]
        anomalyObj.published = obj["published"]
        anomalyObj.save()

def distributeSubTasks(dimValsData, anomalyDefinition):
    """
    Function to distribute anomaly detection sub tasks on medium of choice
    :param anomalyResult: List of dicts, each corresponding to a dimension value
    :param anomalyDefinition: AnomalyDefinition object for which to run anomaly detection services
    """
    createAnomalyObjects(dimValsData, anomalyDefinition)
    anomalyDefProps = {"granularity": anomalyDefinition.dataset.granularity, "highOrLow": anomalyDefinition.highOrLow}
    detectionRuleType = "Prophet"
    detectionParams = {}
    if hasattr(anomalyDefinition, "detectionrule"):
        detectionRuleType = anomalyDefinition.detectionrule.detectionRuleType.name
        detectionParams = {param["param__name"]: param["value"] for param in anomalyDefinition.detectionrule.detectionruleparamvalue_set.all().values("param__name", "value")}

    detectionServicePlatform = os.environ.get("DETECTION_SERVICE_PLATFORM")
    if detectionServicePlatform == "AWS":
        lambdaUrl = os.environ.get("AWS_LAMBDA_URL")
        
        anomalyServiceObjects = [
            {
                "dimValObj": {key: obj[key] for key in ["anomalyId", "dimVal", "contriPercent"]},
                "dfDict": json.loads(obj["df"].to_json()),
                "anomalyDefProps": anomalyDefProps,
                "detectionRuleType": detectionRuleType,
                "detectionParams": detectionParams,
            }   for obj in dimValsData
        ]

        result = asyncio.run(concurrentLambdaRequests(lambdaUrl, anomalyServiceObjects))
    else:
        # Default case is anomaly detection via celery
        detectionJobs = group(
            _anomalyDetectionSubTask.s(
                {key: obj[key] for key in ["anomalyId", "dimVal", "contriPercent"]},
                obj["df"].to_dict("records"),
                anomalyDefProps,
                detectionRuleType,
                detectionParams
            )
            for obj in dimValsData
        )
        _detectionJobs = detectionJobs.apply_async()
        with allow_join_result():
            result = _detectionJobs.get()
        
    saveAnomalyObjects(result)

    return result


@shared_task
def anomalyDetectionJob(anomalyDef_id: int, manualRun: bool = False):
    """
    Method to find initiate anomaly detection for a given anomaly definition
    :param anomalyDef_id: ID of the anomaly definition
    :param manualRun: Boolean determining whether task was manually initiated
    """
    totalAnomalyPublished = 0
    totalAnomalyCount = 0
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
            anomalyDefinition.dataset.isNonRollup,
        )

        result = distributeSubTasks(dimValsData, anomalyDefinition)

        Anomaly.objects.filter(
            id__in=[anomaly["anomalyId"] for anomaly in result if anomaly["success"]]
        ).update(latestRun=runStatusObj)

        logs["numAnomaliesPulished"] = len(
            [anomaly for anomaly in result if anomaly.get("published")]
        )
        logs["numAnomalySubtasks"] = len(dimValsData)
        totalAnomalyPublished = logs["numAnomaliesPulished"]
        totalAnomalyCount = logs["numAnomalySubtasks"]

        logs["log"] = json.dumps(
            {anomaly["dimVal"]: anomaly for anomaly in result}
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
        event_logs(anomalyDef_id,runStatusObj.status,totalAnomalyPublished,totalAnomalyCount)
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

            ############################################################### Webhook Alert #############################################################################
            
            numPublished = logs["numAnomaliesPulished"]
            webhookAlertMessageFormat(numPublished, anomalyDefinition)

    if runStatusObj.status == ANOMALY_DETECTION_ERROR:
        message = (
            "Anomaly Detection Job failed on AnomalyDefintion id : "
            + str(anomalyDef_id)
            + "\n"
        )
        message = message + str(logs["log"])
        name = "appAlert"
        event_logs(anomalyDef_id,runStatusObj.status, totalAnomalyPublished ,totalAnomalyCount )
        SlackAlert.slackAlertHelper(title, message, name)
        
        ############ Webhook Alert ############
        WebHookAlert.webhookAlertHelper(name, title, message)



def webhookAlertMessageFormat(numPublished, anomalyDefinition: AnomalyDefinition):
    """ Format message for webhook URL alert"""
    try:
        textMessage = f"{numPublished} {'anomalies' if numPublished > 1 else 'anomaly'} published. "
        topNtext = (
            f" Top {anomalyDefinition.value}"
            if int(float(anomalyDefinition.value)) > 0
            else ""
        )
        dimText = f" {anomalyDefinition.dimension}" if anomalyDefinition.dimension else ""
        highLowText = f" {anomalyDefinition.highOrLow}" if anomalyDefinition.highOrLow else ""
        textMessage = (
            textMessage
            + f"Anomaly Definition: {anomalyDefinition.metric}{dimText}{highLowText}{topNtext}"+", "
        )
        textMessage = (
            textMessage
            + f"Dataset: {anomalyDefinition.dataset.name}" + ", "
        )
        textMessage = (
            textMessage +  f"Granularity: {anomalyDefinition.dataset.granularity}" + ", "
        )
        highestContriAnomaly = anomalyDefinition.anomaly_set.order_by(
            "data__contribution"
        ).last()
        anomalyId = highestContriAnomaly.id
        data = AnomalySerializer(highestContriAnomaly).data
        templateName = anomalyDefinition.getAnomalyTemplateName()
        cardTemplate = AnomalyCardTemplate.objects.get(templateName=templateName)
        data.update(data["data"]["anomalyLatest"])
        textSubject = (
            html2text.html2text(Template(cardTemplate.title).render(Context(data))).replace("**", "").replace("\n","")
        
        )
        textDetails = Template(cardTemplate.title).render(Context(data)) + " "
        textDetails = textDetails + Template(cardTemplate.bodyText).render(Context(data)) + " "
        textDetails = textDetails.replace("<b>", "").replace("</b>", "")
        name = "anomalyAlert"
        WebHookAlert.webhookAlertHelper(name, textSubject, textMessage, textDetails, anomalyDefinition.id, anomalyId)
    except Exception as ex:
        logger.error("Webhook alert failed ",str(ex))

