"""
Contains urls mapped with Anomalys app views
"""
from django.urls import path
from . import views

urlpatterns = [
    # Anomalys
    path("anomalys", views.AnomalysView.as_view(publishedOnly=True), name="anomalys"),
    path(
        "allanomalys",
        views.AnomalysView.as_view(publishedOnly=False),
        name="allAnomalys",
    ),
    path("anomaly/<int:anomalyId>", views.AnomalyView.as_view(), name="anomaly"),
    # Datasets
    path("datasets", views.DatasetsView.as_view(), name="datasets"),
    path("dataset/<int:datasetId>", views.DatasetView.as_view(), name="dataset"),
    path("dataset/create", views.CreateDatasetView.as_view(), name="createDataset"),
    # Connections
    path("connections", views.connections, name="connections"),
    path("connection/<int:connection_id>", views.connection, name="connection"),
    path("connectiontypes", views.connectionTypes, name="connectionTypes"),
    # Query
    path("runQuery", views.QueryView.as_view(), name="querys"),
    # AnomalyDefinition
    path("anomalyDefs", views.AnomalyDefView.as_view(), name="anomalyDefs"),
    path(
        "anomalyDef/<int:anomalyId>", views.AnomalyDefView.as_view(), name="anomalyDef"
    ),
    path("addAnomalyDef", views.AnomalyDefView.as_view(), name="addAnomalyDef"),
    path("editAnomalyDef", views.AnomalyDefView.as_view(), name="editAnomalyDef"),
    path("runAnomalyDef/<int:anomalyDefId>", views.runAnomalyDef, name="runAnomalyDef"),
    # RunStatus
    path(
        "runStatusAnomalies/<int:runStatusId>",
        views.runStatusAnomalies,
        name="runStatusAnomalies",
    ),
    path(
        "runStatus/<int:anomalyDefId>", views.getDetectionRuns, name="getDetectionRuns"
    ),
    path("isTaskRunning/<int:anomalyDefId>", views.isTaskRunning, name="isTaskRunning"),
    # Schedules
    path("schedules/", views.ScheduleView.as_view(), name="scheduleView"),
    path("schedules/<int:scheduleId>", views.schedule, name="getSingleSchedule"),
    path("timezones/", views.TimzoneView.as_view(), name="timezoneView"),
    path("anomalyDefJob/", views.AnomalyDefJob.as_view(), name="addAnomalyDefSchedule"),
    path(
        "anomalyDefJob/<int:anomalyDefId>",
        views.AnomalyDefJob.as_view(),
        name="deleteAnomalyDefSchedule",
    ),
    # Settings
    path("settings", views.SettingsView.as_view(), name="settings"),
    # DetectionRules
    path("detectionRuleTypes", views.DetectionRuleTypeView.as_view(), name="detectionRuleTypes"),
    # Root Cause Analysis
    path("rca/<int:anomalyId>", views.RCAView.as_view(), name="rca"),
    # Installtion
    path("installationId", views.InstallationView.as_view(), name="installationId" )
]
