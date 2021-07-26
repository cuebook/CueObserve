import json
import pytest
import unittest
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
# from services.anomalys import Anomalys
from anomaly.services.anomalys import Anomalys
from anomaly.models import AnomalyDefinition, Anomaly

@pytest.mark.django_db(transaction=True)
def test_anomalys(client, mocker):
    schedule = mixer.blend("anomaly.customSchedule", name="Test Schedule")
    connection = mixer.blend("anomaly.connection")
    dataset = mixer.blend("anomaly.dataset", granularity='day', name="DB1")

    path = reverse("addAnomalyDef")
    data = {
        "datasetId": dataset.id,
        "measure": "Quantity",
        "dimension": "Category",
        "highOrLow":"",
        "top":"10"
        
    }
    response = client.post(path, data=data, content_type="application/json")

    dataset2 = mixer.blend("anomaly.dataset", granularity='hour', name = "DB2")
    path = reverse("addAnomalyDef")
    data = {
        "datasetId": dataset2.id,
        "measure": "ReturnEntries",
        "dimension": "Brandcode",
        "highOrLow":"high",
        "top":"20"
        
    }

    response = client.post(path, data=data, content_type="application/json")
    anomalyDefId1 = AnomalyDefinition.objects.all()[0].id
    anomalyDefId2 = AnomalyDefinition.objects.all()[1].id

    anomaly1 = mixer.blend("anomaly.anomaly", anomalyDefinition_id=anomalyDefId1)
    anomaly2 = mixer.blend("anomaly.anomaly", anomalyDefinition_id=anomalyDefId2)

    # Get Anomalys
    path = reverse("allAnomalys")
    response = client.get(path)
    assert response.status_code == 200
    anomalyId = response.data["data"]["anomalies"][0]["id"]

    sorter={"columnKey":"datasetName", "order":"ascend"}
    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery="day", sorter = sorter)
    assert res.success == True
    sorter={"columnKey":"datasetName", "order":"descend"}
    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery=None, sorter = sorter)
    assert res.success == True
    sorter={"columnKey":"granularity", "order":"ascend"}
    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery=None, sorter = sorter)
    assert res.success == True
    sorter={"columnKey":"granularity", "order":"descend"}
    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery=None, sorter = sorter)
    assert res.success == True
    sorter={"columnKey":"metric", "order":"ascend"}
    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery=None, sorter = sorter)
    assert res.success == True
    sorter={"columnKey":"metric", "order":"descend"}

    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery=None, sorter = sorter)
    assert res.success == True
    sorter={"columnKey":"dimensionVal", "order":"ascend"}

    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery=None, sorter = sorter)
    assert res.success == True
    sorter={"columnKey":"dimensionVal", "order":"descend"}

    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery=None, sorter = sorter)
    assert res.success == True
    sorter={"columnKey":"anomaly", "order":"ascend"}

    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery=None, sorter = sorter)
    assert res.success == True
    sorter={"columnKey":"anomaly", "order":"descend"}

    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery=None, sorter = sorter)
    assert res.success == True
    sorter={"columnKey":"contribution", "order":"ascend"}

    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery=None, sorter = sorter)
    assert res.success == True
    sorter={"columnKey":"contribution", "order":"descend"}
    res = Anomalys.getAnomalys(publishedOnly=False,offset=0, limit = 50, searchQuery=None, sorter = sorter)
    assert res.success == True








