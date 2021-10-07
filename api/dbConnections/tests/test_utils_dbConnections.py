import pytest
import unittest
from unittest import mock
from dbConnections.utils import limitSql
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from anomaly.models import Connection, ConnectionType, ConnectionParam
from conftest import populate_seed_data


def test_limitSql():
	""" limits sql """
	sql = "SELECT * from limit 234 limIt  3456  "
	newSql = limitSql(sql)
	assert limitSql(sql) == "SELECT * from limit 234 limit 10  "
	assert sql == "SELECT * from limit 234 limIt  3456  "

@pytest.mark.django_db(transaction=True)
def testDbConnection(client, mocker ):
	""" Test DB connection"""
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


@pytest.mark.django_db()
def test_MSSQLConnection(client, populate_seed_data, mocker):
	"""Testing if connection params in seed data are only needed"""
	connectionType = ConnectionType.objects.get(name="MSSQL")
	paramNames = list(ConnectionParam.objects.filter(connectionType=connectionType).values_list("name", flat=True))
	params = {}
	for name in paramNames:
		params[name] = "test"

	mockResponse = mocker.patch(
		"dbConnections.mssql.pyodbc.connect",
		new=mock.MagicMock(
			autospec=True, return_value=True
		),
	)
	mockResponse.start()

	data = {'name': 'test connection', 'description': '', 'connectionType_id': connectionType.id, 'params': params}
	path = reverse("connections")
	response = client.post(path, data, content_type="application/json")	
	assert response.status_code == 200
	assert response.data["success"]
	assert Connection.objects.all().count()

	mockResponse.stop()


@pytest.mark.django_db()
def test_ClickHouseConnection(client, populate_seed_data, mocker):
	"""Testing if connection params in seed data are only needed"""
	connectionType = ConnectionType.objects.get(name="ClickHouse")
	paramNames = list(ConnectionParam.objects.filter(connectionType=connectionType).values_list("name", flat=True))
	params = {}
	for name in paramNames:
		params[name] = "test"

	mockResponse = mocker.patch(
		"dbConnections.clickhouse.ClickHouse.checkConnection",
		new=mock.MagicMock(
			autospec=True, return_value=True
		),
	)
	mockResponse.start()

	data = {'name': 'test connection', 'description': '', 'connectionType_id': connectionType.id, 'params': params}
	path = reverse("connections")
	response = client.post(path, data, content_type="application/json")
	assert response.status_code == 200
	assert response.data["success"]
	assert Connection.objects.all().count()

	mockResponse.stop()
