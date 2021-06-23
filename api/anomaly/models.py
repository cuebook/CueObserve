from django.db import models


# eg. postgres, mysql
class ConnectionType(models.Model):  # no ui
    name = models.CharField(max_length=200, db_index=True, unique=True)
    label = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


# eg. host, username, password
class ConnectionParam(models.Model):  # no ui
    paramName = models.CharField(max_length=200)
    label = models.CharField(max_length=200, blank=True, null=True)
    isEncrypted = models.BooleanField(default=False)
    connectionType = models.ForeignKey(
        ConnectionType, on_delete=models.CASCADE, db_index=True, related_name="connectionTypeParam"
    )
    properties = models.TextField(null=True, blank=True)  # for ui

    def __str__(self):
        return self.connectionType.name + "_" + self.paramName


class Connection(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    connectionType = models.ForeignKey(
        ConnectionType, on_delete=models.CASCADE, db_index=True, related_name="connectionTypeConnection"
    )
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Anomaly(models.Model):
    connection = models.ForeignKey(Connection, on_delete=models.CASCADE, db_index=True)
    granularity = models.CharField(max_length=20)
    measure = models.CharField(max_length=500)
    dimension = models.CharField(max_length=500, null=True, blank=True)
    topCount = models.IntegerField(default=10)
    highOrLow = models.CharField(max_length=4, default="", blank=True, null=True)
    data = models.JSONField(default=dict)

