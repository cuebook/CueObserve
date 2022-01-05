import logging
from typing import List
from utils.apiResponse import ApiResponse
from anomaly.models import (
    AnomalyDefinition,
    Dataset,
    CustomSchedule as Schedule,
    DetectionRule,
    DetectionRuleParam,
    DetectionRuleParamValue,
    RunStatus,
)
from anomaly.serializers import AnomalyDefinitionSerializer, RunStatusSerializer
from django_celery_beat.models import PeriodicTask, PeriodicTasks, CrontabSchedule
from ops.tasks import anomalyDetectionJob
from django.db.models import Q, Max

RUN_STATUS_LIMIT = 10


class AnomalyDefinitions:
    @staticmethod
    def getAllAnomalyDefinition(
        offset: int = 0, limit: int = 50, searchQuery: str = None, sorter: dict = {}
    ):
        """
        This method is used to get all anomlayObj
        """
        response = ApiResponse("Error in getting Anomaly Definition !")
        anomalyDefObjs = AnomalyDefinition.objects.all().order_by("-id")
        count = anomalyDefObjs.count()

        if searchQuery:
            anomalyDefObjs = AnomalyDefinitions.searchOnAnomalyDefinition(
                anomalyDefObjs, searchQuery
            )
            count = anomalyDefObjs.count()
        if sorter.get("order", False):
            anomalyDefObjs = AnomalyDefinitions.sortOnAnomalyDefinition(
                anomalyDefObjs, sorter
            )
        anomalyDefObjs = anomalyDefObjs[offset : offset + limit]
        anomalyDefData = AnomalyDefinitionSerializer(anomalyDefObjs, many=True).data
        data = {"anomalyDefinition": anomalyDefData, "count": count}

        response.update(True, "AnomalyDefinitions retrived successfully !", data)

        return response

    @staticmethod
    def searchOnAnomalyDefinition(anomalyDefObjs, searchQuery):
        """
        Search on AnomalyDefinition
        """
        return anomalyDefObjs.filter(
            Q(dataset__name__icontains=searchQuery)
            | Q(dataset__granularity__icontains=searchQuery)
            | Q(metric__icontains=searchQuery)
            | Q(highOrLow__icontains=searchQuery)
            | Q(dimension__icontains=searchQuery)
            | Q(value__icontains=searchQuery)
            | Q(operation__icontains=searchQuery)
        )

    @staticmethod
    def sortOnAnomalyDefinition(anomalyDefObjs: List[AnomalyDefinition], sorter):
        """
        Sort Anomaly Definition on given user column
        """
        columnToSort = sorter.get("columnKey", "")
        order = sorter.get("order", "")
        sortingPrefix = "" if order == "ascend" else "-"

        if columnToSort == "datasetName":
            anomalyDefObjs = anomalyDefObjs.order_by(sortingPrefix + "dataset__name")

        if columnToSort == "granularity":
            anomalyDefObjs = anomalyDefObjs.order_by(
                sortingPrefix + "dataset__granularity"
            )

        if columnToSort == "anomalyDef":
            anomalyDefObjs = anomalyDefObjs.order_by(sortingPrefix + "metric")

        if columnToSort == "lastRun":
            anomalyDefObjs = anomalyDefObjs.annotate(
                latestRun=Max("runstatus__startTimestamp")
            ).order_by(sortingPrefix + "latestRun")
            return anomalyDefObjs

        if columnToSort == "lastRunStatus":
            anomalyDefObjs = anomalyDefObjs.annotate(
                latestRun=Max("runstatus__status")
            ).order_by(sortingPrefix + "latestRun")

        return anomalyDefObjs

    @staticmethod
    def addAnomalyDefinition(
        metric: str = None,
        dimension: str = None,
        operation: str = None,
        highOrLow: str = None,
        value: int = 0,
        datasetId: int = 0,
        detectionRuleTypeId: int = 1,
        detectionRuleParams: dict = {},
    ):
        """
        This method is used to add anomaly to AnomalyDefinition table
        """
        response = ApiResponse("Error in creating Anomaly Definition !")
        anomalyObj = AnomalyDefinition.objects.create(
            dataset_id=datasetId,
            metric=metric,
            dimension=dimension,
            highOrLow=highOrLow,
            value=value,
            operation=operation,
        )
        detectionRule = DetectionRule.objects.create(
            detectionRuleType_id=detectionRuleTypeId, anomalyDefinition=anomalyObj
        )
        detectionParams = []
        for param in detectionRuleParams.keys():
            detectionRuleParamObj = DetectionRuleParam.objects.filter(
                name=param
            ).first()
            if detectionRuleParamObj:
                detectionParams.append(
                    DetectionRuleParamValue(
                        param=detectionRuleParamObj,
                        detectionRule=detectionRule,
                        value=str(detectionRuleParams[param]),
                    )
                )
        DetectionRuleParamValue.objects.bulk_create(detectionParams)
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
        response.update(True, "Anomaly Definition successfully deleted !")
        return response

    @staticmethod
    def editAnomalyDefinition(
        anomalyId: int = 0, highOrLow: str = None, detectionRuleParams: dict = {}
    ):
        """
        Update anomaly objects of given anomalyId
        """
        response = ApiResponse("Error in updating Anomaly Definition !")
        anomalyObj = AnomalyDefinition.objects.get(id=anomalyId)
        anomalyObj.highOrLow = highOrLow
        anomalyObj.save()
        if detectionRuleParams:
            originalParams = list(
                anomalyObj.detectionrule.detectionruleparamvalue_set.all()
            )
            for param in originalParams:
                if detectionRuleParams.get(param.param.name):
                    param.value = detectionRuleParams.get(param.param.name)
            DetectionRuleParamValue.objects.bulk_update(originalParams, ["value"])
        response.update(True, "Anomaly Definition updated successfully !")
        return response

    @staticmethod
    def runAnomalyDetection(anomalyDefId: int):
        """
        Run anomaly detection on anomaly definition
        :param anomalyDefId: ID of the anomaly definition
        """
        response = ApiResponse("Error in initiating anomaly detection task")
        anomalyDetectionJob.delay(anomalyDefId, True)
        response.update(True, "Successfully initiated anomaly detection task")
        return response

    @staticmethod
    def getDetectionRuns(anomalyDefId: int, runStatusOffset: int = 0):
        """
        Service to fetch run status details of the selected AnomalyDefinition
        :param anomalyDefId: ID of the Anomaly Definition
        :param runStatusOffset: Offset for fetching run statuses
        """
        res = ApiResponse()
        runStatusData = {}
        runStatuses = RunStatus.objects.filter(
            anomalyDefinition_id=anomalyDefId
        ).order_by("-startTimestamp")[
            runStatusOffset : runStatusOffset + RUN_STATUS_LIMIT
        ]
        runStatuseCount = RunStatus.objects.filter(
            anomalyDefinition_id=anomalyDefId
        ).count()
        runStatusData["runStatuses"] = RunStatusSerializer(runStatuses, many=True).data
        runStatusData["count"] = runStatuseCount
        res.update(True, "Run statuses retrieved successfully", runStatusData)
        return res

    @staticmethod
    def isTaskRunning(anomalyDefId: int):
        """
        Service to check whether a task is running for anomaly definition
        :param anomalyDefId: ID of the Anomaly Definition
        """
        res = ApiResponse()
        lastRunStatus = RunStatus.objects.filter(anomalyDefinition_id=anomalyDefId).order_by("-startTimestamp").first()
        
        taskRunning = False
        if lastRunStatus:
            taskRunning = lastRunStatus.status == "RUNNING"
        res.update(True, "Task Running status checked.", {"isRunning": taskRunning})
        return res

    @staticmethod
    def runStatusAnomalies(runStatusId: int):
        """
        Service to fetch anomalies of a RunStatus and their metadata
        :param anomalyDefId: ID of the Anomaly Definition
        """
        res = ApiResponse()
        runStatus = RunStatus.objects.get(id=runStatusId)
        anomaliesData = list(
            runStatus.anomaly_set.all().values("dimensionVal", "id", "published")
        )
        res.update(True, "Run status anomalies retrieved successfully", anomaliesData)
        return res


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
        ptask = PeriodicTask.objects.update_or_create(
            name=anomalyDefId,
            defaults={
                "crontab": cronSchedule,
                "task": anomalyDetectionJob.name,
                "args": f'["{anomalyDefId}"]',
            },
        )
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
