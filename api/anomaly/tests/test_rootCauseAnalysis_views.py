import pytest
import unittest
import pandas as pd
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer

from anomaly.models import RCAAnomaly
from ops.tasks import rootCauseAnalysisJob
from ops.tasks.rootCauseAnalysis import _anomalyDetectionForValue

@pytest.mark.django_db(transaction=True)
def test_rootCauseAnalysis(client, mocker):
    """
    """
    anomalyData = {
            'anomalyLatest': {'highOrLow': 'low',
             'value': 2.0,
             'percent': 37,
             'anomalyTimeISO': '2021-08-07T13:00:00',
             'anomalyTime': 1628244000000.0,
             'contribution': 5.71},
            'contribution': 5.71
        }
    dataset = mixer.blend("anomaly.dataset", granularity="hour", metrics='["Returns"]', dimensions='["City", "ColorCode", "BrandCode"]', timestampColumn="Date")
    anomalyDefinition = mixer.blend("anomaly.anomalyDefinition", dimension="BrandCode", metric="Returns", dataset=dataset, periodicTask=None, operation="Top", value=10)
    anomaly = mixer.blend("anomaly.anomaly", anomalyDefinition=anomalyDefinition, dimensionVal="XBRZ", data=anomalyData)

    data = [{'City': 'Bangalore', 'BrandCode': "XBRZ", 'Date': '2021-08-07T20:00:00.000Z', 'ColorCode': 'PINK', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-07T17:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 1},
         {'City': 'Amritsar', 'BrandCode': "XBRZ", 'Date': '2021-08-07T10:00:00.000Z', 'ColorCode': 'OCHRE', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-07T13:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 28},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-07T13:00:00.000Z', 'ColorCode': 'BROWN', 'Returns': 48},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-07T08:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Kolkata', 'BrandCode': "XBRZ", 'Date': '2021-08-07T05:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 1},
         {'City': 'Hyderabad', 'BrandCode': "XBRZ", 'Date': '2021-08-06T18:00:00.000Z', 'ColorCode': 'OCHRE', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-06T16:00:00.000Z', 'ColorCode': 'MUSTARD', 'Returns': 16},
         {'City': 'Block Head Quarters', 'BrandCode': "XBRZ", 'Date': '2021-08-06T12:00:00.000Z', 'ColorCode': 'OCHRE', 'Returns': 16},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-06T11:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Hyderabad', 'BrandCode': "XBRZ", 'Date': '2021-08-06T11:00:00.000Z', 'ColorCode': 'OFF WHITE', 'Returns': 16},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-06T09:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 16},
         {'City': 'Bikaner', 'BrandCode': "XBRZ", 'Date': '2021-08-06T07:00:00.000Z', 'ColorCode': 'CORAL', 'Returns': 16},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-06T07:00:00.000Z', 'ColorCode': 'LILAC', 'Returns': 16},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-06T07:00:00.000Z', 'ColorCode': 'SKY BLUE', 'Returns': 16},
         {'City': 'Greater Thane', 'BrandCode': "XBRZ", 'Date': '2021-08-06T04:00:00.000Z', 'ColorCode': 'PINK', 'Returns': 1},
         {'City': 'Indore', 'BrandCode': "XBRZ", 'Date': '2021-08-05T14:00:00.000Z', 'ColorCode': 'SEA GREEN', 'Returns': 16},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-05T12:00:00.000Z', 'ColorCode': 'PEACH', 'Returns': 16},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-05T11:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Surat', 'BrandCode': "XBRZ", 'Date': '2021-08-05T12:00:00.000Z', 'ColorCode': 'BLACK', 'Returns': 1},
         {'City': 'Basti', 'BrandCode': "XBRZ", 'Date': '2021-08-05T11:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Hyderabad', 'BrandCode': "XBRZ", 'Date': '2021-08-05T11:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 1},
         {'City': 'Kolkata', 'BrandCode': "XBRZ", 'Date': '2021-08-05T11:00:00.000Z', 'ColorCode': 'RED', 'Returns': 1},
         {'City': 'Vadodara', 'BrandCode': "XBRZ", 'Date': '2021-08-05T11:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 16},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-05T10:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 16},
         {'City': 'Davangere', 'BrandCode': "XBRZ", 'Date': '2021-08-05T09:00:00.000Z', 'ColorCode': 'CORAL', 'Returns': 16},
         {'City': 'Indore', 'BrandCode': "XBRZ", 'Date': '2021-08-05T09:00:00.000Z', 'ColorCode': 'GREEN', 'Returns': 16},
         {'City': 'Pune', 'BrandCode': "XBRZ", 'Date': '2021-08-05T07:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 16},
         {'City': 'Noida', 'BrandCode': "XBRZ", 'Date': '2021-08-05T02:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 9},
         {'City': 'Kolkata', 'BrandCode': "XBRZ", 'Date': '2021-08-04T17:00:00.000Z', 'ColorCode': 'SEA BLUE', 'Returns': 16},
         {'City': 'MUMBAI', 'BrandCode': "XBRZ", 'Date': '2021-08-04T17:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 16},
         {'City': 'Jaipur', 'BrandCode': "XBRZ", 'Date': '2021-08-04T14:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 16},
         {'City': 'Hyderabad', 'BrandCode': "XBRZ", 'Date': '2021-08-04T13:00:00.000Z', 'ColorCode': 'BLACK', 'Returns': 16},
         {'City': 'Hyderabad', 'BrandCode': "XBRZ", 'Date': '2021-08-04T13:00:00.000Z', 'ColorCode': 'CORAL', 'Returns': 16},
         {'City': 'Hyderabad', 'BrandCode': "XBRZ", 'Date': '2021-08-04T13:00:00.000Z', 'ColorCode': 'RED', 'Returns': 16},
         {'City': 'Varanasi', 'BrandCode': "XBRZ", 'Date': '2021-08-04T10:00:00.000Z', 'ColorCode': 'SKY BLUE', 'Returns': 1},
         {'City': 'Indore', 'BrandCode': "XBRZ", 'Date': '2021-08-04T05:00:00.000Z', 'ColorCode': 'PEACH', 'Returns': 3},
         {'City': 'Kanpur', 'BrandCode': "XBRZ", 'Date': '2021-08-03T17:00:00.000Z', 'ColorCode': 'BLUE', 'Returns': 16},
         {'City': 'Pune', 'BrandCode': "XBRZ", 'Date': '2021-08-03T11:00:00.000Z', 'ColorCode': 'OFF WHITE', 'Returns': 16},
         {'City': 'Ghaziabad', 'BrandCode': "XBRZ", 'Date': '2021-08-03T10:00:00.000Z', 'ColorCode': 'PISTACHIO', 'Returns': 1},
         {'City': 'Greater Thane', 'BrandCode': "XBRZ", 'Date': '2021-08-03T10:00:00.000Z', 'ColorCode': 'YELLOW', 'Returns': 1},
         {'City': 'Ghaziabad', 'BrandCode': "XBRZ", 'Date': '2021-08-03T07:00:00.000Z', 'ColorCode': 'YELLOW', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-03T04:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 16},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-02T15:00:00.000Z', 'ColorCode': 'PINK', 'Returns': 16},
         {'City': 'Amravati', 'BrandCode': "XBRZ", 'Date': '2021-08-02T14:00:00.000Z', 'ColorCode': 'YELLOW', 'Returns': 3},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-02T13:00:00.000Z', 'ColorCode': 'WHITE', 'Returns': 3},
         {'City': 'Bangalore', 'BrandCode': "XBRZ", 'Date': '2021-08-02T10:00:00.000Z', 'ColorCode': 'PINK', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-02T10:00:00.000Z', 'ColorCode': 'SEA GREEN', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-02T13:00:00.000Z', 'ColorCode': 'CREAM', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-02T12:00:00.000Z', 'ColorCode': 'OCHRE', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-02T11:00:00.000Z', 'ColorCode': 'OFF WHITE', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-02T10:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-02T09:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-02T08:00:00.000Z', 'ColorCode': 'YELLOW', 'Returns': 1},
         {'City': 'Kolkata', 'BrandCode': "XBRZ", 'Date': '2021-08-02T07:00:00.000Z', 'ColorCode': 'BLACK', 'Returns': 3},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-02T06:00:00.000Z', 'ColorCode': 'LILAC', 'Returns': 9},
         {'City': 'Hyderabad', 'BrandCode': "XBRZ", 'Date': '2021-08-02T06:00:00.000Z', 'ColorCode': 'CORAL', 'Returns': 9},
         {'City': 'Hyderabad', 'BrandCode': "XBRZ", 'Date': '2021-08-02T06:00:00.000Z', 'ColorCode': 'RED', 'Returns': 9},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-08-02T06:00:00.000Z', 'ColorCode': 'YELLOW', 'Returns': 1},
         {'City': 'Bangalore', 'BrandCode': "XBRZ", 'Date': '2021-08-02T05:00:00.000Z', 'ColorCode': 'CORAL', 'Returns': 1},
         {'City': 'Pune', 'BrandCode': "XBRZ", 'Date': '2021-08-02T05:00:00.000Z', 'ColorCode': 'WHITE', 'Returns': 1},
         {'City': 'Pune', 'BrandCode': "XBRZ", 'Date': '2021-08-02T03:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 1},
         {'City': 'Indore', 'BrandCode': "XBRZ", 'Date': '2021-08-01T18:00:00.000Z', 'ColorCode': 'SEA GREEN', 'Returns': 16},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-08-01T12:00:00.000Z', 'ColorCode': 'BLACK', 'Returns': 3},
         {'City': 'Kolkata', 'BrandCode': "XBRZ", 'Date': '2021-08-01T03:00:00.000Z', 'ColorCode': 'BLACK', 'Returns': 9},
         {'City': 'Jaipur', 'BrandCode': "XBRZ", 'Date': '2021-07-31T15:00:00.000Z', 'ColorCode': 'PINK', 'Returns': 16},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-07-31T12:00:00.000Z', 'ColorCode': 'BLUE', 'Returns': 1},
         {'City': 'Greater Thane', 'BrandCode': "XBRZ", 'Date': '2021-07-31T12:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-31T11:00:00.000Z', 'ColorCode': 'DENIM REGULAR', 'Returns': 1},
         {'City': 'Kolkata', 'BrandCode': "XBRZ", 'Date': '2021-07-31T07:00:00.000Z', 'ColorCode': 'OFF WHITE', 'Returns': 3},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-31T07:00:00.000Z', 'ColorCode': 'FUCHSIA', 'Returns': 1},
         {'City': 'Ghaziabad', 'BrandCode': "XBRZ", 'Date': '2021-07-31T06:00:00.000Z', 'ColorCode': 'NATURAL', 'Returns': 1},
         {'City': 'Hyderabad', 'BrandCode': "XBRZ", 'Date': '2021-07-31T06:00:00.000Z', 'ColorCode': 'CORAL', 'Returns': 9},
         {'City': 'Hyderabad', 'BrandCode': "XBRZ", 'Date': '2021-07-31T06:00:00.000Z', 'ColorCode': 'RED', 'Returns': 9},
         {'City': 'Kolkata', 'BrandCode': "XBRZ", 'Date': '2021-07-31T06:00:00.000Z', 'ColorCode': 'BLACK', 'Returns': 1},
         {'City': 'Gwalior', 'BrandCode': "XBRZ", 'Date': '2021-07-31T04:00:00.000Z', 'ColorCode': 'SEA GREEN', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-31T04:00:00.000Z', 'ColorCode': 'YELLOW', 'Returns': 1},
         {'City': 'Bhadohi', 'BrandCode': "XBRZ", 'Date': '2021-07-31T03:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 9},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-30T16:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 1},
         {'City': 'Kolkata', 'BrandCode': "XBRZ", 'Date': '2021-07-30T14:00:00.000Z', 'ColorCode': 'GREY', 'Returns': 1},
         {'City': 'Patna', 'BrandCode': "XBRZ", 'Date': '2021-07-30T13:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Pune', 'BrandCode': "XBRZ", 'Date': '2021-07-30T10:00:00.000Z', 'ColorCode': 'BLACK', 'Returns': 1},
         {'City': 'Lucknow', 'BrandCode': "XBRZ", 'Date': '2021-07-30T09:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 9},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-30T09:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Pune', 'BrandCode': "XBRZ", 'Date': '2021-07-30T09:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Bangalore', 'BrandCode': "XBRZ", 'Date': '2021-07-30T07:00:00.000Z', 'ColorCode': 'SKY BLUE', 'Returns': 1},
         {'City': 'Ghaziabad', 'BrandCode': "XBRZ", 'Date': '2021-07-30T07:00:00.000Z', 'ColorCode': 'GREY', 'Returns': 1},
         {'City': 'Ghaziabad', 'BrandCode': "XBRZ", 'Date': '2021-07-30T07:00:00.000Z', 'ColorCode': 'PURPLE', 'Returns': 1},
         {'City': 'Meerut', 'BrandCode': "XBRZ", 'Date': '2021-07-30T07:00:00.000Z', 'ColorCode': 'WHITE', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-07-30T07:00:00.000Z', 'ColorCode': 'RED', 'Returns': 1},
         {'City': 'Chennai', 'BrandCode': "XBRZ", 'Date': '2021-07-30T06:00:00.000Z', 'ColorCode': 'BLACK', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-07-30T05:00:00.000Z', 'ColorCode': 'RED', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-30T05:00:00.000Z', 'ColorCode': 'PINK', 'Returns': 1},
         {'City': 'SITAPUR', 'BrandCode': "XBRZ", 'Date': '2021-07-30T05:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 16},
         {'City': 'Kolhapur', 'BrandCode': "XBRZ", 'Date': '2021-07-30T04:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Surat', 'BrandCode': "XBRZ", 'Date': '2021-07-30T04:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Buldhana', 'BrandCode': "XBRZ", 'Date': '2021-07-30T03:00:00.000Z', 'ColorCode': 'BLUE MELANGE', 'Returns': 16},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-07-29T13:00:00.000Z', 'ColorCode': 'BLUE', 'Returns': 3},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-07-29T13:00:00.000Z', 'ColorCode': 'GREY', 'Returns': 3},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-07-29T09:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 1},
         {'City': 'Deoria', 'BrandCode': "XBRZ", 'Date': '2021-07-29T09:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 1},
         {'City': 'Lucknow', 'BrandCode': "XBRZ", 'Date': '2021-07-29T09:00:00.000Z', 'ColorCode': 'LILAC', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-29T09:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 1},
         {'City': 'Amritsar', 'BrandCode': "XBRZ", 'Date': '2021-07-29T08:00:00.000Z', 'ColorCode': 'BLACK', 'Returns': 1},
         {'City': 'Thane', 'BrandCode': "XBRZ", 'Date': '2021-07-29T07:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 1},
         {'City': 'Hyderabad', 'BrandCode': "XBRZ", 'Date': '2021-07-29T06:00:00.000Z', 'ColorCode': 'YELLOW', 'Returns': 1},
         {'City': 'Lucknow', 'BrandCode': "XBRZ", 'Date': '2021-07-29T06:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Pune', 'BrandCode': "XBRZ", 'Date': '2021-07-29T06:00:00.000Z', 'ColorCode': 'FUCHSIA', 'Returns': 1},
         {'City': 'Kolkata', 'BrandCode': "XBRZ", 'Date': '2021-07-29T05:00:00.000Z', 'ColorCode': 'RUST', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-29T05:00:00.000Z', 'ColorCode': 'TEAL', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-07-29T04:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-29T04:00:00.000Z', 'ColorCode': 'BLACK', 'Returns': 1},
         {'City': 'Gwalior', 'BrandCode': "XBRZ", 'Date': '2021-07-28T18:00:00.000Z', 'ColorCode': 'NATURAL', 'Returns': 1},
         {'City': 'Gwalior', 'BrandCode': "XBRZ", 'Date': '2021-07-28T18:00:00.000Z', 'ColorCode': 'RED', 'Returns': 1},
         {'City': 'Davangere', 'BrandCode': "XBRZ", 'Date': '2021-07-28T16:00:00.000Z', 'ColorCode': 'CORAL', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-28T15:00:00.000Z', 'ColorCode': 'AQUA', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-28T13:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-28T13:00:00.000Z', 'ColorCode': 'OFF WHITE', 'Returns': 1},
         {'City': 'Kolkata', 'BrandCode': "XBRZ", 'Date': '2021-07-28T11:00:00.000Z', 'ColorCode': 'FUCHSIA', 'Returns': 1},
         {'City': 'Bangalore', 'BrandCode': "XBRZ", 'Date': '2021-07-28T05:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 1},
         {'City': 'Lucknow', 'BrandCode': "XBRZ", 'Date': '2021-07-27T10:00:00.000Z', 'ColorCode': 'NATURAL', 'Returns': 1},
         {'City': 'Pune', 'BrandCode': "XBRZ", 'Date': '2021-07-27T10:00:00.000Z', 'ColorCode': 'PINK', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-07-27T07:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-07-27T06:00:00.000Z', 'ColorCode': 'ROYAL BLUE', 'Returns': 9},
         {'City': 'Pune', 'BrandCode': "XBRZ", 'Date': '2021-07-26T17:00:00.000Z', 'ColorCode': 'CORAL', 'Returns': 1},
         {'City': 'Kolkata', 'BrandCode': "XBRZ", 'Date': '2021-07-26T16:00:00.000Z', 'ColorCode': 'WHITE', 'Returns': 1},
         {'City': 'Indore', 'BrandCode': "XBRZ", 'Date': '2021-07-26T15:00:00.000Z', 'ColorCode': 'YELLOW', 'Returns': 1},
         {'City': 'Bengaluru', 'BrandCode': "XBRZ", 'Date': '2021-07-26T11:00:00.000Z', 'ColorCode': 'NAVY', 'Returns': 1},
         {'City': 'Mumbai', 'BrandCode': "XBRZ", 'Date': '2021-07-26T10:00:00.000Z', 'ColorCode': 'MULTI', 'Returns': 1},
         {'City': 'Delhi', 'BrandCode': "XBRZ", 'Date': '2021-07-26T08:00:00.000Z', 'ColorCode': 'WHITE', 'Returns': 1}]

    df = pd.DataFrame(data=data)

    mockFetchDatasetDataframe = mocker.patch(
        "access.data.Data.fetchDatasetDataframe",
        new=mock.MagicMock(
            autospec=True, return_value=df
        ),
    )
    mockFetchDatasetDataframe.start()

    def dummyParallelizeAnomalyDetection(anomalyId: int, dimension: str, dimValsData: list):
        """
        Runs anomaly detection in series
        """
        return [
            _anomalyDetectionForValue(
                anomalyId,
                dimension,
                obj["dimVal"],
                obj["contriPercent"],
                obj["df"].to_dict("records"),
            ) for obj in dimValsData
        ]

    mockParallelizeAnomalyDetection = mocker.patch(
        "ops.tasks.rootCauseAnalysis._parallelizeAnomalyDetection",
        new=mock.MagicMock(
            autospec=True, side_effect=dummyParallelizeAnomalyDetection
        ),
    )
    mockParallelizeAnomalyDetection.start()

    rootCauseAnalysisJob(anomaly.id)

    mockFetchDatasetDataframe.stop()
    mockParallelizeAnomalyDetection.stop()

    assert RCAAnomaly.objects.count() == 2

    # testing get rca call 

    path = reverse("rca", kwargs={"anomalyId": anomaly.id})
    response = client.get(path)

    assert response.status_code == 200
    assert response.data['data'] == {
         'anomalyContribution': 5.71,
         'granularity': 'hour',
         'anomalyTime': '2021-08-07T13:00:00',
         'dimension': 'BrandCode',
         'dimensionValue': 'XBRZ',
         'endTimestamp': response.data['data']['endTimestamp'],
         'logs': {'Analyzing Dimensions': 'City, ColorCode',
                  'City': 'Analyzed',
                  'ColorCode': 'Analyzed'},
         'measure': 'Returns',
         'rcaAnomalies': response.data['data']['rcaAnomalies'],
         'startTimestamp': response.data['data']['startTimestamp'],
         'status': 'SUCCESS',
         'value': 2.0}

    assert list(response.data['data']['rcaAnomalies'][0].keys()) == ['dimension', 'dimensionValue', 'data']



@pytest.mark.django_db(transaction=True)
def test_calculateRCA(client, mocker):

    mockRCAJob = mocker.patch(
        "ops.tasks.rootCauseAnalysis.rootCauseAnalysisJob.delay",
        new=mock.MagicMock(
            autospec=True, return_value=True
        ),
    )
    mockRCAJob.start()

    anomalyDefinition = mixer.blend("anomaly.anomalyDefinition", periodicTask=None)
    anomaly = mixer.blend("anomaly.anomaly", anomalyDefinition=anomalyDefinition) 
    path = reverse("rca", kwargs={"anomalyId": anomaly.id})
    response = client.post(path)

    assert response.status_code == 200
    assert response.data['success']

    mockRCAJob.stop()
