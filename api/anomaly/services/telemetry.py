import analytics
import random
import string
import os
import json
import logging
from utils.apiResponse import ApiResponse
from anomaly.models import AnomalyDefinition, Dataset, InstallationTable, Connection, Setting
analytics.write_key = 'euY80DdHK2wT3LuehjDlQEzsriLQkZG6'

logger = logging.getLogger(__name__)


def getInstallationId():
    """ Function to get installation, if exists or create one"""
    try:
        res = ApiResponse()
        userId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

        if not InstallationTable.objects.all().exists():
            userId = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
            dbType = ""
            if os.environ.get("POSTGRES_DB_HOST", False):
                dbType = "postgres"
            else:
                dbType = "sqlite"
            userObj = InstallationTable.objects.create(installationId = userId, databaseType = dbType)
            
            data = {"installationId": userObj.installationId}
            res.update(True, "Installation Id created and fetched successfully", data)
        else:
            installId = InstallationTable.objects.all()[0].installationId
            data = {"installationId": installId}
            res.update(True, "Installation Id fetched successfully", data)
        return res

    except Exception as ex:
        logger.error("Exception occured while creating installtion userId %s", str(ex))
        data = {"installationId": "UnIdentified"}
        res.update(False, "Error while fetching installation Id", data)
        return res


def event_logs(anomalyDef_id,status, publishedCount, totalCount):
    """Event logs on anomaly definition Run"""
    userId = "UnIdentified"
    try:
        # userObject = InstallationTable.objects.all()[0]
        # userId = userObject.installationId
        res = getInstallationId()
        userId = res.data.get("installationId","UnIdentified")
        traits = update_traits()
        adf = AnomalyDefinition.objects.get(id=anomalyDef_id)
        datasetConnection = adf.dataset.connection.connectionType.name
        datasetGranularity = adf.dataset.granularity
        datasetDimensionsCount = len(json.loads(adf.dataset.dimensions)) if adf.dataset.dimensions else ""
        datasetMeasuresCount = len(json.loads(adf.dataset.metrics)) if adf.dataset.metrics else ""
        split = "Y" if adf.dimension else "N"
        splitLimit = adf.operation
        algorithm = adf.detectionrule.detectionRuleType.name
        definitionOperation = adf.operation if adf.operation else ""
        definitionHighOrLow = adf.highOrLow if adf.highOrLow else ""
        operationValue = adf.value if adf.value else ""
        definitionString = definitionOperation + " " + operationValue + " " + definitionHighOrLow
        scheduleCron = "* * * * *"
        scheduleTimeZone = ""
        if adf.periodicTask:
            scheduleCron = adf.periodicTask.crontab.minute + adf.periodicTask.crontab.hour + adf.periodicTask.crontab.day_of_month + adf.periodicTask.crontab.month_of_year + adf.periodicTask.crontab.day_of_week 
            scheduleTimeZone = adf.periodicTask.crontab.timezone.zone
        
        analytics.track(userId, 'AnomalyRan', {
            "datasetConnection": datasetConnection,
            "datasetGranularity": datasetGranularity,		
            "datasetDimensions": datasetDimensionsCount,
            "datasetMeasures": datasetMeasuresCount,
            "split": split,
            "splitLimit": splitLimit,			
            "algorithm": algorithm,		
            "definitionString": definitionString, 
            "scheduleCron": scheduleCron,
            "scheduleTimeZone": scheduleTimeZone,
            "runStatus": status,
            "anomaliesPublished": publishedCount,
            "anomaliesTotal": totalCount
        })

    except Exception as ex:
        analytics.track(userId, 'AnomalyRan', {
            "exception": str(ex)
        })




def update_traits():
    """ Update user traits on every event log"""
    try:
        userObject = InstallationTable.objects.all()[0]
        userId = userObject.installationId
        createdAt = userObject.createdAt
        connCount = Connection.objects.all().count()
        datasetCount = Dataset.objects.all().count()
        anomalyObjs = AnomalyDefinition.objects.all()
        settings = Setting.objects.exclude(value="").count()
        anomalyDefCount = anomalyObjs.count()
        anomalyDefinitionScheduleCount = 0
        for obj in anomalyObjs:
            if obj.periodicTask:
                anomalyDefinitionScheduleCount += 1

        analytics.identify(userId, {
        
        "createdAt": createdAt,  # Read from table , trigger at every event_log while anomaly definition run
        "connections": connCount,
        "datasets": datasetCount,
        "anomalyDefinitions": anomalyDefCount,
        "anomalyDefinitionsScheduled": anomalyDefinitionScheduleCount,
        "settings": settings,
        })
        return True
    except Exception as ex:
        return False

def rca_event_log(status):
    """Event log on RCA run"""
    userId = "UnIdentified"
    try:
        res = getInstallationId()
        userId = res.data.get("installationId","UnIdentified")
        traits = update_traits()
        analytics.track(userId, "RCARan",{
            "runStatus": status
        })
    except Exception as ex:
        analytics.track(userId, "RCARan",{
            "exception": str(ex)
        })







