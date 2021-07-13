import logging
from typing import List
from utils.apiResponse import ApiResponse
from dbConnections import BigQuery
from anomaly.models import AnomalyDefinition, Dataset, CustomSchedule as Schedule
from anomaly.serializers import AnomalyDefinitionSerializer
from django_celery_beat.models import PeriodicTask, PeriodicTasks, CrontabSchedule
from ops.tasks import anomalyDetectionJob

CELERY_TASK_NAME = "ops.tasks.anomalyDetectionJob"

class AnomalyDefinitions:

    @staticmethod
    def getAllAnomalyDefinition():
        """
        This method is used to get all anomlayObj
        """

        response = ApiResponse("Error in getting Anomaly Definition !")
        anomalyDef = AnomalyDefinition.objects.all().order_by("-id")
        anomalyDefSerializer = AnomalyDefinitionSerializer(anomalyDef, many=True)
        response.update(True, "AnomalyDefinitions retrived successfully !", anomalyDefSerializer.data)

        return response

    @staticmethod
    def addAnomalyDefinition(metric: str = None, dimension: str = None, highOrLow: str = None, top: int = 0, datasetId: int = 0):
        """
        This method is used to add anomaly to AnomalyDefinition table
        """
        response = ApiResponse("Error in creating Anomaly Definition !")
        anomalyObj = AnomalyDefinition.objects.create(
            dataset_id=datasetId,
            metric=metric,
            dimension=dimension,
            highOrLow=highOrLow,
            top=top
        )
        response.update(True, "Anomaly Definition created successfully !")
        return response

    @staticmethod
    def deleteAnomalyDefinition(anomalyId):
        """
        Delete anomaly objects of given id
        """
        response = ApiResponse("Error in creating Anomaly Definition !")
        anomalyObj = AnomalyDefinition.objects.get(id=anomalyId)
        anomalyObj.delete()
        response.update(True,"Anomaly Definition successfully deleted !")
        return response

    @staticmethod
    def editAnomalyDefinition(anomalyId: int = 0, highOrLow: str = None):
        """
        Update anomaly objects of given anomalyId
        """
        response = ApiResponse("Error in updating Anomaly Definition !")
        anomalyObj = AnomalyDefinition.objects.get(id=anomalyId)
        anomalyObj.highOrLow = highOrLow
        anomalyObj.save()
        response.update(True, "Anomaly Definition updated successfully !")
        return response
    
    @staticmethod
    def runAnomalyDetection(anomalyDefId: int):
        """
        Run anomaly detection on anomaly definition
        :param anomalyDefId: ID of the anomaly definition
        """
        response = ApiResponse("Error in initiating anomaly detection task")
        anomalyDetectionJob.delay(anomalyDefId)
        response.update(True, "Successfully initiated anomaly detection task")
        return response

        
class AnomalyDefJobServices:
    @staticmethod
    def addAnomalyDefJob(anomalyDefId: str, scheduleId: int):
        """
        Service to add a new AnomalyDefJob
        :param anomalyDefId: ID of the AnomalyDef for which to create job
        :param scheduleId: ID of schedule
        """
        res = ApiResponse()
        scheduleObj = Schedule.objects.get(id=scheduleId)
        cronSchedule = scheduleObj.cronSchedule
        ptask = PeriodicTask.objects.update_or_create(name = anomalyDefId ,defaults={"crontab" : cronSchedule, "task" : CELERY_TASK_NAME, "args" : f'["{anomalyDefId}"]'})
        anomalyDefObj = AnomalyDefinition.objects.get(id=anomalyDefId)
        anomalyDefObj.periodicTask = ptask
        anomalyDefObj.periodicTask.save()
        anomalyDefObj.save()
        res.update(True, "AnomalyDefJob added successfully", None)
        return res

    @staticmethod
    def deleteAnomalyDefJob(anomalyDefId: int):
        """
        Service to update crontab of an existing AnomalyDefJob
        :param anomalyDefId: ID of the AnomalyDef for which to delete
        """
        res = ApiResponse()
        anomalyDefObj = AnomalyDefinition.objects.get(id=anomalyDefId)
        anomalyDefObj.periodicTask = None
        anomalyDefObj.save()
        res.update(True, "AnomalyDefJob deleted successfully", None)
        return res
