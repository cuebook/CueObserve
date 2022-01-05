import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpRequest

from anomaly.services import (
    Datasets,
    Connections,
    Querys,
    AnomalyDefinitions,
    Anomalys,
    ScheduleService,
    AnomalyDefJobServices,
    Settings,
    DetectionRules,
    RootCauseAnalyses,
)
from anomaly.services.telemetry import getInstallationId


class AnomalysView(APIView):
    """
    Provides views on datasets(many)
    """

    publishedOnly = False

    def get(self, request):
        """get request"""
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 50))
        searchQuery = request.GET.get("searchText", "")
        sorter = json.loads(request.GET.get("sorter", "{}"))
        res = Anomalys.getAnomalys(
            publishedOnly=self.publishedOnly,
            offset=offset,
            limit=limit,
            searchQuery=searchQuery,
            sorter=sorter,
        )
        return Response(res.json())


class AnomalyView(APIView):
    """
    Provided views on Dataset(single)
    """

    def get(self, request, anomalyId: int):
        """get request"""
        res = Anomalys.getAnomaly(anomalyId)
        return Response(res.json())


class DatasetsView(APIView):
    """
    Provides views on datasets(many)
    """

    def get(self, request):
        """get request"""
        res = Datasets.getDatasets()
        return Response(res.json())


class DatasetView(APIView):
    """
    Provided views on Dataset(single)
    """

    def get(self, request, datasetId: int):
        """get request"""
        res = Datasets.getDataset(datasetId)
        return Response(res.json())

    def post(self, request, datasetId: int):
        """post request"""
        data = request.data
        res = Datasets.updateDataset(datasetId, data)
        return Response(res.json())

    def delete(self, request, datasetId: int):
        """delete request"""
        res = Datasets.deleteDataset(datasetId)
        return Response(res.json())


class CreateDatasetView(APIView):
    """
    Provides view on creating Dataset
    """

    def post(self, request):
        """post request"""
        data = request.data
        res = Datasets.createDataset(data)
        return Response(res.json())


# TODO
# class for connections
@api_view(["GET", "POST"])
def connections(request: HttpRequest) -> Response:
    """
    Method to get or add connection
    :param request: HttpRequest
    """
    if request.method == "GET":
        res = Connections.getConnections()
        return Response(res.json())
    elif request.method == "POST":
        res = Connections.addConnection(request.data)
        return Response(res.json())


@api_view(["GET", "PUT", "DELETE"])
def connection(request: HttpRequest, connection_id: int) -> Response:
    """
    Method for crud operations on a single connection
    :param request: HttpRequest
    :param connection_id: Connection Id
    """
    if request.method == "GET":
        res = Connections.getConnection(connection_id)
        return Response(res.json())
    elif request.method == "DELETE":
        res = Connections.removeConnection(connection_id)
        return Response(res.json())
    elif request.method == "PUT":
        res = Connections.updateConnection(connection_id, request.data)
        return Response(res.json())


@api_view(["GET", "POST"])
def connectionTypes(request: HttpRequest) -> Response:
    """
    Method to get all connection types
    :param request: HttpRequest
    """
    if request.method == "GET":
        res = Connections.getConnectionTypes()
        return Response(res.json())


class QueryView(APIView):
    """
    Provides view on creating Dataset
    """

    def post(self, request):
        """post request"""
        data = request.data
        sql = data["sql"]
        connectionId = data["connectionId"]
        connectionType, connectionParams = Connections.getConnectionParams(connectionId)
        res = Querys.runQuery(connectionType, connectionParams, sql)
        return Response(res.json())


class AnomalyDefView(APIView):
    """
    Provides view on Anomaly Operation
    """

    def get(self, request):
        offset = int(request.GET.get("offset", 0))
        limit = int(request.GET.get("limit", 50))
        searchQuery = request.GET.get("searchText", "")
        sorter = json.loads(request.GET.get("sorter", "{}"))
        res = AnomalyDefinitions.getAllAnomalyDefinition(
            offset=offset, limit=limit, searchQuery=searchQuery, sorter=sorter
        )
        return Response(res.json())

    def post(self, request):
        datasetId = int(request.data.get("datasetId", 0))
        metric = request.data.get("measure", None)
        highOrLow = request.data.get("highOrLow", None)
        operation = request.data.get("operation", None)
        value = request.data.get("operationValue", 0)
        dimension = request.data.get("dimension", None)
        detectionRuleTypeId = request.data.get("detectionRuleTypeId", 1)
        detectionRuleParams = request.data.get("detectionRuleParams", {})
        res = AnomalyDefinitions.addAnomalyDefinition(
            metric,
            dimension,
            operation,
            highOrLow,
            value,
            datasetId,
            detectionRuleTypeId,
            detectionRuleParams,
        )
        return Response(res.json())

    def delete(self, request, anomalyId: int):
        res = AnomalyDefinitions.deleteAnomalyDefinition(anomalyId)
        return Response(res.json())

    def put(self, request):
        anomalyDefId = request.data.get("anomalyDefId", 0)
        highOrLow = request.data.get("highOrLow", None)
        detectionRuleParams = request.data.get("detectionRuleParams", {})
        res = AnomalyDefinitions.editAnomalyDefinition(anomalyDefId, highOrLow, detectionRuleParams)
        return Response(res.json())


class ScheduleView(APIView):
    """
    Class to get and add available crontab schedules
    """

    def get(self, request):
        res = ScheduleService.getSchedules()
        return Response(res.json())

    def post(self, request):
        name = request.data["name"]
        cron = request.data["crontab"]
        timezone = request.data["timezone"]
        res = ScheduleService.addSchedule(cron=cron, timezone=timezone, name=name)
        return Response(res.json())

    def put(self, request):
        id = request.data["id"]
        name = request.data["name"]
        crontab = request.data["crontab"]
        timezone = request.data["timezone"]
        res = ScheduleService.updateSchedule(
            id=id, crontab=crontab, timezone=timezone, name=name
        )
        return Response(res.json())


@api_view(["GET", "PUT", "DELETE"])
def schedule(request: HttpRequest, scheduleId: int) -> Response:
    """
    Method for crud operations on a single connection
    :param request: HttpRequest
    :param connection_id: Connection Id
    """
    if request.method == "GET":
        res = ScheduleService.getSingleSchedule(scheduleId)
        return Response(res.json())
    if request.method == "DELETE":
        res = ScheduleService.deleteSchedule(scheduleId)
        return Response(res.json())


class TimzoneView(APIView):
    """
    Class to get standard pytz timezones
    """

    def get(self, request):
        res = ScheduleService.getTimezones()
        return Response(res.json())


class AnomalyDefJob(APIView):
    """
    Class to get, add and update a NotebookJob details
    The put and post methods only require request body and not path parameters
    The get method requires the notebookJobId as the path parameter
    """

    # def get(self, request, notebookId=None):
    #     offset = int(request.GET.get("offset", 0))
    #     res = AnomalyDefJobServices.getNotebookJobDetails(notebookId=notebookId, runStatusOffset=offset)
    #     return Response(res.json())

    def post(self, request):
        anomalyDefId = request.data["anomalyDefId"]
        scheduleId = request.data["scheduleId"]
        res = AnomalyDefJobServices.addAnomalyDefJob(
            anomalyDefId=anomalyDefId, scheduleId=scheduleId
        )
        return Response(res.json())

    def delete(self, request, anomalyDefId=None):
        res = AnomalyDefJobServices.deleteAnomalyDefJob(anomalyDefId=anomalyDefId)
        return Response(res.json())


@api_view(["POST"])
def runAnomalyDef(request: HttpRequest, anomalyDefId: int) -> Response:
    """
    Method for run anomaly detection for a given anomaly definition
    :param request: HttpRequest
    :param anomalyDefId: ID of the anomaly definition
    """
    res = AnomalyDefinitions.runAnomalyDetection(anomalyDefId)
    return Response(res.json())


@api_view(["GET"])
def runStatusAnomalies(request: HttpRequest, runStatusId: int) -> Response:
    """
    Method for fetch anomalies of a RunStatus and their urls
    :param request: HttpRequest
    :param anomalyDefId: ID of the anomaly definition
    """
    res = AnomalyDefinitions.runStatusAnomalies(runStatusId)
    return Response(res.json())


@api_view(["GET"])
def getDetectionRuns(request: HttpRequest, anomalyDefId: int) -> Response:
    """
    Method for fetching run statuses for a given anomaly definition
    :param request: HttpRequest
    :param anomalyDefId: ID of the anomaly definition
    """
    offset = int(request.GET.get("offset", 0))
    res = AnomalyDefinitions.getDetectionRuns(anomalyDefId, offset)
    return Response(res.json())


@api_view(["GET"])
def isTaskRunning(request: HttpRequest, anomalyDefId: int) -> Response:
    """
    Method for checking whether anomaly task is running
    :param request: HttpRequest
    :param anomalyDefId: ID of the anomaly definition
    """
    res = AnomalyDefinitions.isTaskRunning(anomalyDefId)
    return Response(res.json())


class SettingsView(APIView):
    """
    Provides views on settings
    """

    def get(self, request):
        """get request"""
        res = Settings.getSettings()
        return Response(res.json())

    def post(self, request):
        """post request"""
        data = request.data
        res = Settings.updateSettings(data)
        return Response(res.json())


class DetectionRuleTypeView(APIView):
    """
    Provides views on Detection Rule Types
    """

    def get(self, request):
        """get request"""
        res = DetectionRules.getDetectionRuleTypes()
        return Response(res.json())


class RCAView(APIView):
    """
    Provides views on RCA (Root Cause Analysis)
    """

    def get(self, request, anomalyId: int):
        """get rca"""
        res = RootCauseAnalyses.getRCA(anomalyId)
        return Response(res.json())

    def post(self, request, anomalyId: int):
        """make RCA request"""
        res = RootCauseAnalyses.calculateRCA(anomalyId)
        return Response(res.json())

    def delete(self, request, anomalyId: int):
        """make RCA request"""
        res = RootCauseAnalyses.abortRCA(anomalyId)
        return Response(res.json())

class InstallationView(APIView):
    """ Provides views on Installation """
    def get(self, request):
        res = getInstallationId()
        return Response(res.json())