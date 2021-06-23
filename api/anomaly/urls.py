from django.urls import path
from . import views

urlpatterns = [
	path("anomalys", views.AnomalysView.as_view(), name="anomalys")
]