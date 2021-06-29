import pytest
import unittest
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer

@pytest.mark.django_db(transaction=True)
def test_datasets(client, mocker):

    # Create workflow test
    path = reverse('datasets')
    response = client.get(path)
    assert response.status_code == 200
