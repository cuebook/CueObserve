import pytest
import unittest
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer

@pytest.mark.django_db(transaction=True)
def test_connections(client, mocker):
    """
    Test case for connections
    """

    # Add Connection
    connectionType = mixer.blend("anomaly.connectionType")
    ConnectionParam = mixer.blend("anomaly.ConnectionParam", connectionType = connectionType, name="file")
    path = reverse("connections")
    mockResponse = mocker.patch(
        "dbConnections.bigquery.BigQuery.checkConnection",
        new=mock.MagicMock(
            autospec=True, return_value=True
        ),
    )
    mockResponse.start()
    data = {'name': 'test', 'description': '', 'connectionType_id': connectionType.id,
     'params': {'file': '{   "type": "service_account",   "project_id": "Test",   "private_key_id": "LFDJKQWOUER0PQEU09348",   "private_key": "-----BEGIN PRIVATE KEY-----\\Not Exists\\n-----END PRIVATE KEY-----\\n",   "client_email": "test@gmail.com",   "client_id": "test",   "auth_uri": "https://accounts.google.com/o/oauth2/auth",   "token_uri": "https://oauth2.googleapis.com/token",   "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",   "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/test" }'
    }}
    response = client.post(path, data, content_type="application/json")
    mockResponse.stop()

    assert response.data["success"]
    assert response.status_code == 200
    
    # Get All Connections
    path = reverse("connections")
    response = client.get(path)
    connectionId = response.data["data"][0]["id"]
    assert response.data["success"]
    assert response.status_code == 200

    # Get single connection
    path = reverse("connection", kwargs={"connection_id":connectionId })
    response = client.get(path)
    assert response.data["success"]
    assert response.status_code == 200
    
    # Get connectionType
    path = reverse("connectionTypes")
    response = client.get(path)
    assert response.data["success"]
    assert response.status_code == 200
    
    # Remove connection
    path = reverse("connection", kwargs={"connection_id":connectionId })
    response = client.delete(path)
    assert response.data["success"]
    assert response.status_code == 200
    











