import pytest
import unittest
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from users.models import CustomUser

@pytest.fixture()
def setup_user(db):
    """sets up a user to be used for login"""
    user = CustomUser.objects.create_superuser("admin@domain.com", "admin")
    user.status = "Active"
    user.is_active = True
    user.name = "Sachin"
    user.save()

@pytest.mark.django_db(transaction=True)
def test_datasets(setup_user, client, mocker):
    client.login(email="admin@domain.com", password="admin")

    # Get dataset when no entry
    path = reverse('datasets')
    response = client.get(path)
    assert response.status_code == 200
    assert not response.data['data']


    # Create dataset
    connection = mixer.blend("anomaly.connection")

    path = reverse("createDataset")
    data = {
        "name": "something",
        "sql": "SELECT * from TEST_TABLE",
        "connectionId": connection.id,
        "metrics": ["Amount", "Quantity"],
        "dimensions": ["Category", "Region"],
        "timestamp": "CreatedAt",
        "granularity": "day"
    }
    response = client.post(path, data=data, content_type="application/json")

    assert response.status_code == 200
    assert response.data['success'] 

    # Get datasets
    path = reverse('datasets')
    response = client.get(path)
    assert response.status_code == 200
    assert response.data['data']
    assert set(response.data['data'][0].keys()) == set(['anomalyDefinitionCount', 'connection', 'granularity', 'name', 'id','connectionName'])

    dataset = response.data['data'][0]


    # Get dataset
    path = reverse("dataset", kwargs={"datasetId": dataset['id']})
    response = client.get(path)

    assert response.status_code == 200
    assert response.data['data']
    assert response.data['data']['name'] == "something"
    assert set(response.data['data'].keys()) == set(['id', 'name', 'sql', 'connection', 'dimensions', 'metrics', 'granularity', 'timestampColumn', 'anomalyDefinitionCount'])


    # Update dataset
    data = {
        "name": "anything",
        "sql": "SELECT * from TEST_TABLE",
        "connectionId": connection.id,
        "metrics": ["Amount", "Quantity"],
        "dimensions": ["Category", "Region"],
        "timestamp": "CreatedAt",
        "granularity": "day"
    }
    path = reverse("dataset", kwargs={"datasetId": dataset['id']})
    response = client.post(path, data=data, content_type="application/json")
    assert response.status_code == 200
    assert response.data['success']

    # Get dataset
    path = reverse("dataset", kwargs={"datasetId": dataset['id']})
    response = client.get(path)

    assert response.status_code == 200
    assert response.data['data']
    assert response.data['data']['name'] == "anything"


    # Delete dataset
    path = reverse("dataset", kwargs={"datasetId": dataset['id']})
    response = client.delete(path)

    assert response.status_code == 200
    assert response.data['success']


    # Get datasets
    path = reverse('datasets')
    response = client.get(path)
    assert response.status_code == 200
    assert not response.data['data']

