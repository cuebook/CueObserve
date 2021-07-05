"""
Contains urls mapped with Anomalys app views
"""
from django.urls import path
from . import views

urlpatterns = [
    # Anomalys
    path("anomalys", views.AnomalysView.as_view(), name="anomalys"),
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
    path("editAnomalyDef",  views.AnomalyDefView.as_view(), name="editAnomalyDef")
]
