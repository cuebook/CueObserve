# pylint: disable=C0115
from typing import DefaultDict, Dict
from django.db import models

# from django_celery_beat.models import  CrontabSchedule, PeriodicTask


# eg. postgres, mysql
class ConnectionType(models.Model):  # no ui
    name = models.CharField(max_length=200, db_index=True, unique=True)
    label = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


# eg. host, username, password
class ConnectionParam(models.Model):  # no ui
    name = models.CharField(max_length=200)
    label = models.CharField(max_length=200, blank=True, null=True)
    isEncrypted = models.BooleanField(default=False)
    connectionType = models.ForeignKey(
        ConnectionType,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="connectionTypeParam",
    )
    properties = models.JSONField(null=True, blank=True)  # for ui

    def __str__(self):
        return self.connectionType.name + "_" + self.name


class Connection(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    connectionType = models.ForeignKey(
        ConnectionType,
        on_delete=models.CASCADE,
        db_index=True,
        related_name="connectionTypeConnection",
    )
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ConnectionParamValue(models.Model):
    connectionParam = models.ForeignKey(
        ConnectionParam, on_delete=models.CASCADE, related_name="cpvcp"
    )
    value = models.TextField()
    connection = models.ForeignKey(
        Connection, on_delete=models.CASCADE, related_name="cpvc"
    )


class Dataset(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, db_index=True)
    name = models.CharField(max_length=500)
    sql = models.TextField(null=True, blank=True)
    granularity = models.CharField(max_length=50)
    timestampColumn = models.CharField(max_length=500)
    metrics = models.TextField(null=True, blank=True)
    dimensions = models.TextField(null=True, blank=True)


class AnomalyDefinition(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, db_index=True)
    metric = models.TextField(null=True, blank=True)
    dimension = models.TextField(null=True, blank=True)
    highOrLow = models.TextField(null=True, blank=True)
    value = models.CharField(default=0, max_length=500)
    operation = models.CharField(null=True, blank=True, max_length=500)
    periodicTask = models.OneToOneField(
        "django_celery_beat.PeriodicTask",
        on_delete=models.SET_NULL,
        db_index=True,
        null=True,
    )

class RunStatus(models.Model):
    """
    Model class to store logs and statuses of NotebookJob runs
    """

    startTimestamp = models.DateTimeField(auto_now_add=True)
    endTimestamp = models.DateTimeField(null=True, default=None)
    anomalyDefinition = models.ForeignKey(
        AnomalyDefinition, on_delete=models.CASCADE, db_index=True
    )
    status = models.CharField(max_length=20)
    runType = models.CharField(max_length=20, blank=True, null=True)  # Manual/Scheduled
    logs = models.JSONField(default=dict)

class Anomaly(models.Model):
    anomalyDefinition = models.ForeignKey(
        AnomalyDefinition, on_delete=models.CASCADE, db_index=True
    )
    dimensionVal = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=False)
    data = models.JSONField(default=dict)
    latestRun = models.ForeignKey(RunStatus, on_delete=models.SET_NULL, null=True, default=None)


class AnomalyCardTemplate(models.Model):
    templateName = models.CharField(
        blank=True, null=True, db_index=True, max_length=500
    )
    title = models.TextField(blank=True, null=True)
    bodyText = models.TextField(blank=True, null=True)
    supportedVariables = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.templateName


class CustomSchedule(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    cronSchedule = models.ForeignKey(
        "django_celery_beat.CrontabSchedule", on_delete=models.CASCADE, db_index=True
    )


class Setting(models.Model):
    """
    Model class to store settings/config related to application
    """

    name = models.TextField(null=True, blank=True)
    value = models.TextField(null=True, blank=True)
