# pylint: disable=C0115
from typing import DefaultDict, Dict
from django.db import models


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
    properties = models.TextField(null=True, blank=True)  # for ui
    file = models.JSONField(default=dict)

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
    file = models.JSONField(default=dict)

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
