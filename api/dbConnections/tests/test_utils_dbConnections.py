import pytest
import unittest
from unittest import mock
from dbConnections.utils import limitSql

def test_limitSql():
	""" limits sql """
	sql = "SELECT * from limIt  3456"
	assert limitSql(sql) == "SELECT * from limit 10"
	assert sql == "SELECT * from limIt  3456"
