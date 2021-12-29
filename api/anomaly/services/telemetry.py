import analytics
import os
import json
from anomaly.models import AnomalyDefinition, Dataset, InstallationTable, Connection
analytics.write_key = 'euY80DdHK2wT3LuehjDlQEzsriLQkZG6'

def event_logs(anomalyDef_id,status, publishedCount, totalCount):
    """Event logs on anomaly definition Run"""
    userObject = InstallationTable.objects.all()[0]
    userId = userObject.installationId
    traits = update_traits(userObject)
    adf = AnomalyDefinition.objects.get(id=anomalyDef_id)
    datasetConnection = adf.dataset.connection.name
    datasetGranularity = adf.dataset.granularity
    datasetDimensionsCount = len(json.loads(adf.dataset.dimensions)) if adf.dataset.dimensions else ""
    datasetMeasuresCount = len(json.loads(adf.dataset.metrics)) if adf.dataset.metrics else ""
    split = "Y" if adf.dimension else "N"
    splitLimit = adf.operation
    algorithm = adf.detectionrule.detectionRuleType.name
    definitionOperation = adf.operation if adf.operation else ""
    definitionHighOrLow = adf.highOrLow if adf.highOrLow else ""
    definitionString = definitionOperation + " " + definitionHighOrLow
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



def update_traits(userObject):
    """ Update user traits on every event log"""
    try:
        # userObject = InstallationTable.objects.all()[0]
        userId = userObject.installationId
        createdAt = userObject.createdAt
        connCount = Connection.objects.all().count()
        datasetCount = Dataset.objects.all().count()
        anomalyObjs = AnomalyDefinition.objects.all()
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
        })
        return True
    except Exception as ex:
        return False

def rca_event_log(status):
    """Event log on RCA run"""
    userObject = InstallationTable.objects.all()[0]
    userId = userObject.installationId
    traits = update_traits(userObject)
    analytics.track(userId, "RCARan",{
        "runStatus": status
    })


