import pytest
import unittest
from unittest import mock
import json
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from anomaly.models import AnomalyDefinition
from anomaly.services.anomalyDefinitions import AnomalyDefinitions


@pytest.mark.django_db(transaction=True)
def test_anomalyDefinition(client, mocker):
    """
    Test cases for anomalyDefinition
    """
    schedule = mixer.blend("anomaly.customSchedule", name="Test Schedule")
    # Get anomlay when no entry
    path = reverse('anomalyDefs')
    response = client.get(path)
    assert response.status_code == 200
    
    assert not response.data['data']["anomalyDefinition"]
    assert response.data["data"]["count"] == 0

    # Create anomaly
    connection = mixer.blend("anomaly.connection")
    detectionRuleType = mixer.blend("anomaly.DetectionRuleType", id=1, name="Prophet")
    dataset = mixer.blend("anomaly.dataset", granularity='day')

    path = reverse("addAnomalyDef")
    data = {
        "datasetId": dataset.id,
        "measure": "Quantity",
        "dimension": "Category",
        "highOrLow":"",
        "operation":"Top",
        "value":"10"
        
    }
    response = client.post(path, data=data, content_type="application/json")

    assert response.status_code == 200
    assert response.data['success'] 
    # Get anomalys
    path = reverse('anomalyDefs')
    response = client.get(path)
    assert response.status_code == 200
    assert response.data['data']["anomalyDefinition"]
    anomaly = response.data['data']["anomalyDefinition"][0]["anomalyDef"]

    # Update anomalys
    path = reverse('editAnomalyDef')
    data = {
        "anomalyDefId":anomaly["id"],
        "highOrLow":"Low"
    }
    response = client.put(path, data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.data


    # Add Schedule to AnomalyDefinition
    path = reverse("addAnomalyDefSchedule")
    data = {'anomalyDefId': anomaly["id"], 'scheduleId': schedule.id}
    response = client.post(path, data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.data

    # Delete Schedule From AnomalyDefinition
    path = reverse("deleteAnomalyDefSchedule", kwargs={'anomalyDefId': anomaly["id"]})
    response = client.delete(path)
    assert response.status_code == 200
    assert response.data
    
    dataset1 = mixer.blend("anomaly.dataset", granularity='hour')

    path = reverse("addAnomalyDef")
    data = {
        "datasetId": dataset1.id,
        "measure": "ReturnEntries",
        "dimension": "Brandcode",
        "highOrLow":"high",
        "operation":"Top",
        "value":"10"
        
    }

    response = client.post(path, data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.data['success'] 
    sorter = {"columnKey":"datasetName", "order":"ascend"}
    res = AnomalyDefinitions.getAllAnomalyDefinition(offset=0,limit=50,searchQuery="day",sorter=sorter)
    res.success == True
    sorter = {"columnKey":"granularity", "order":"ascend"}
    res = AnomalyDefinitions.getAllAnomalyDefinition(offset=0,limit=50,searchQuery=None,sorter=sorter)
    res.success == True
    sorter = {"columnKey":"anomalyDef", "order":"ascend"}
    res = AnomalyDefinitions.getAllAnomalyDefinition(offset=0,limit=50,searchQuery=None,sorter=sorter)
    res.success == True
    sorter = {"columnKey":"lastRun", "order":"ascend"}
    res = AnomalyDefinitions.getAllAnomalyDefinition(offset=0,limit=50,searchQuery=None,sorter=sorter)
    res.success == True
    sorter = {"columnKey":"lastRunStatus", "order":"ascend"}
    res = AnomalyDefinitions.getAllAnomalyDefinition(offset=0,limit=50,searchQuery=None,sorter=sorter)
    res.success == True
    

    # Delete anomalys
    path = reverse('anomalyDef', kwargs={"anomalyId": anomaly["id"]})
    response = client.delete(path)
    assert response.status_code == 200
    assert response.data
