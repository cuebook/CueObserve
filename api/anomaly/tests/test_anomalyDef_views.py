import pytest
import unittest
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer

@pytest.mark.django_db(transaction=True)
def test_anomalys(client, mocker):

    # Get anomlay when no entry
    path = reverse('anomalys')
    response = client.get(path)
    assert response.status_code == 200
    assert not response.data['data']


    # Create anomaly
    connection = mixer.blend("anomaly.connection")
    dataset = mixer.blend("anomaly.dataset", granularity='day')

    path = reverse("addAnomaly")
    data = {
        "datasetId": dataset.id,
        "metric": "Quantity",
        "dimension": "Category",
        "highOrLow":"",
        "top":"10"
        
    }
    response = client.post(path, data=data, content_type="application/json")

    assert response.status_code == 200
    assert response.data['success'] 


    # Get anomalys
    path = reverse('anomalys')
    response = client.get(path)
    assert response.status_code == 200
    assert response.data['data']

    dataset = response.data['data'][0]
