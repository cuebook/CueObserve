import pytest
import unittest
from unittest import mock
from dbConnections.utils import limitSql

def test_limitSql():
	""" limits sql """
	sql = "SELECT * from limit 234 limIt  3456  "
	newSql = limitSql(sql)
	assert limitSql(sql) == "SELECT * from limit 234 limit 10  "
	assert sql == "SELECT * from limit 234 limIt  3456  "
