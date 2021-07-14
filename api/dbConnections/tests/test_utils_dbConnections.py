import pytest
import unittest
from unittest import mock
from dbConnections.utils import limitSql
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from anomaly.models import Connection

def test_limitSql():
	""" limits sql """
	sql = "SELECT * from limit 234 limIt  3456  "
	newSql = limitSql(sql)
	assert limitSql(sql) == "SELECT * from limit 234 limit 10  "
	assert sql == "SELECT * from limit 234 limIt  3456  "

@pytest.mark.django_db(transaction=True)
def testDbConnection(client, mocker ):
	""" Test DB connection"""

	connectionType = mixer.blend("anomaly.connectionType", name= "Druid")
	mixer.blend("anomaly.connectionParam", connectionType = connectionType, name ="host")
	mixer.blend("anomaly.connectionParam", connectionType = connectionType, name ="port")
	path = reverse("connections")

	mockResponse = mocker.patch(
		"dbConnections.druid.Druid.checkConnection",
		new=mock.MagicMock(
			autospec=True, return_value=True
		),
	)
	mockResponse.start()
	data = {'name': 'test druid', 'description': '', 'connectionType_id': connectionType.id, 'params': {'host': 'localhost', 'port': '8888'}}
	response = client.post(path, data, content_type="application/json")
	mockResponse.stop()
	assert response.status_code == 200
	assert response.data["success"]
	assert Connection.objects.all().count() == 1
	