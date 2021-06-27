from django.urls import path
from . import views

urlpatterns = [
	path("anomalys", views.AnomalysView.as_view(), name="anomalys"),
	# Connections
	path("connections", views.connections, name="connections"),
    path("connection/<int:connection_id>", views.connection, name="connection"),
    path("connectiontypes", views.connectionTypes, name="connectionTypes"),
]