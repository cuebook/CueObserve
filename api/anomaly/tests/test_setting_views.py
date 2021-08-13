import pytest
import unittest
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from utils.apiResponse import ApiResponse


@pytest.mark.django_db(transaction=True)
def test_setting(client, mocker):
    # Create setting test
    path = reverse('settings')
    res = ApiResponse("Successfully tested setting")
    mockResponse = mocker.patch(
        "anomaly.services.settings.Settings.updateSettings",
        new=mock.MagicMock(
            autospec=True, return_value=res
        ),
    )
    mockResponse.start()
    data = {
        "Anomaly Alert via Slack Webhook Url": "test1URL",
        "App Alerts via Slack Webhook Url": "test2URL"
    }
    response = client.post(path, data=data, content_type="application/json")
    assert response.status_code == 200

    # Get setting test
    path = reverse("settings")
    response = client.get(path)
    assert response.status_code == 200
    assert len(response.data["data"]) == 2