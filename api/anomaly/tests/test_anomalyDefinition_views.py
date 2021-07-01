import pytest
import unittest
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from anomaly.models import AnomalyDefinition

@pytest.mark.django_db(transaction=True)
def test_anomalyDefinition(client, mocker):
    """
    Test cases for anomalyDefinition
    """

    # Get anomlay when no entry
    path = reverse('anomalyDefs')
    response = client.get(path)
    assert response.status_code == 200
    assert not response.data['data']

    # Create anomaly
    connection = mixer.blend("anomaly.connection")
    dataset = mixer.blend("anomaly.dataset", granularity='day')

    path = reverse("addAnomalyDef")
    data = {
        "datasetId": dataset.id,
        "measure": "Quantity",
        "dimension": "Category",
        "highOrLow":"",
        "top":"10"
        
    }
    response = client.post(path, data=data, content_type="application/json")

    assert response.status_code == 200
    assert response.data['success'] 

    # Get anomalys
    path = reverse('anomalyDefs')
    response = client.get(path)
    assert response.status_code == 200
    assert response.data['data']
    anomaly = response.data['data'][0]["anomalyDef"]

    #Delete anomalys
    path = reverse('anomalyDefs', kwargs={"anomalyId": anomaly["id"]})
    response = client.delete(path)
    assert response.status_code == 200
    assert response.data


