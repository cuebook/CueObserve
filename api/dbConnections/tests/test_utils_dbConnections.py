import pytest
import unittest
from unittest import mock
from dbConnections.utils import limitSql
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from anomaly.models import Connection
from users.models import CustomUser

@pytest.fixture()
def setup_user(db):
    """sets up a user to be used for login"""
    user = CustomUser.objects.create_superuser("admin@domain.com", "admin")
    user.status = "Active"
    user.is_active = True
    user.name = "Sachin"
    user.save()

def test_limitSql():
	""" limits sql """
	sql = "SELECT * from limit 234 limIt  3456  "
	newSql = limitSql(sql)
	assert limitSql(sql) == "SELECT * from limit 234 limit 10  "
	assert sql == "SELECT * from limit 234 limIt  3456  "

@pytest.mark.django_db(transaction=True)
def testDbConnection(setup_user, client, mocker ):
	""" Test DB connection"""
	client.login(email="admin@domain.com", password="admin")

	# Test cases for Druid connection 
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

	# Test cases for Postgres connection
	postgresConnectionType = mixer.blend("anomaly.connectionType", name= "Postgres")
	mixer.blend("anomaly.connectionParam", connectionType = postgresConnectionType, name ="host")
	mixer.blend("anomaly.connectionParam", connectionType = postgresConnectionType, name ="port")
	mixer.blend("anomaly.connectionParam", connectionType = postgresConnectionType, name ="database")
	mixer.blend("anomaly.connectionParam", connectionType = postgresConnectionType, name ="username")
	mixer.blend("anomaly.connectionParam", connectionType = postgresConnectionType, name ="password")


	path = reverse("connections")

	mockResponse = mocker.patch(
		"dbConnections.postgres.Postgres.checkConnection",
		new=mock.MagicMock(
			autospec=True, return_value=True
		),
	)
	mockResponse.start()
	data = {'name': 'test connection', 'description': '', 'connectionType_id': postgresConnectionType.id, 'params': {'host': 'Location where postgres db is hosted', 'database': 'db name', 'port': '25060', 'username': 'username', 'password': '******'}}
	response = client.post(path, data, content_type="application/json")	
	mockResponse.stop()

	assert response.status_code == 200
	assert response.data["success"]
	assert Connection.objects.all().count() == 2

	# Test cases for MySQL connection  
	mysqlConnectionType = mixer.blend("anomaly.connectionType", name= "MySQL")
	mixer.blend("anomaly.connectionParam", connectionType = mysqlConnectionType, name ="host")
	mixer.blend("anomaly.connectionParam", connectionType = mysqlConnectionType, name ="port")
	mixer.blend("anomaly.connectionParam", connectionType = mysqlConnectionType, name ="database")
	mixer.blend("anomaly.connectionParam", connectionType = mysqlConnectionType, name ="username")
	mixer.blend("anomaly.connectionParam", connectionType = mysqlConnectionType, name ="password")


	path = reverse("connections")

	mockResponse = mocker.patch(
		"dbConnections.mysql.MySQL.checkConnection",
		new=mock.MagicMock(
			autospec=True, return_value=True
		),
	)
	mockResponse.start()
	data = {'name': 'test connection', 'description': '', 'connectionType_id': mysqlConnectionType.id, 'params': {'host': 'Location where postgres db is hosted', 'database': 'db name', 'port': '25060', 'username': 'username', 'password': '******'}}
	response = client.post(path, data, content_type="application/json")	
	mockResponse.stop()

	assert response.status_code == 200
	assert response.data["success"]
	assert Connection.objects.all().count() == 3


