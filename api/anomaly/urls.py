"""
Contains urls mapped with Anomalys app views
"""
from django.urls import path
from . import views

urlpatterns = [
    # ============ datasets ==================
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
    path("anomalyDefs", views.AnomalyView.as_view(), name="anomalyDefs"),
    path("anomalyDefs/<int:anomalyId>",views.AnomalyView.as_view(), name="anomalyDefs"),
    path("addAnomalyDef", views.AnomalyView.as_view(), name="addAnomalyDef")
]
