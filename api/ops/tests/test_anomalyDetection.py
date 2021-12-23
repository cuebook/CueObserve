import pytest
from unittest import mock
from ops.tasks.detection.core.anomalyDetection import anomalyService
from anomaly.models import Anomaly
from pandas import Timestamp
from mixer.backend.django import mixer
import pandas as pd

@pytest.mark.django_db(transaction=True)
def test_createAnomalyService(client, mocker):
    fakedata = [{'ds': Timestamp('2021-06-01 00:00:00+0000', tz='UTC'),
        'y': 1.0},
        {'ds': Timestamp('2021-06-02 00:00:00+0000', tz='UTC'),
        'y': 1.0},
        {'ds': Timestamp('2021-06-03 00:00:00+0000', tz='UTC'), 'y': 0.0},
        {'ds': Timestamp('2021-06-04 00:00:00+0000', tz='UTC'), 'y': 0.0},
        {'ds': Timestamp('2021-06-05 00:00:00+0000', tz='UTC'),
        'y': 4.0},
        {'ds': Timestamp('2021-06-06 00:00:00+0000', tz='UTC'), 'y': 0.0},
        {'ds': Timestamp('2021-06-07 00:00:00+0000', tz='UTC'),
        'y': 4.0},
        {'ds': Timestamp('2021-06-08 00:00:00+0000', tz='UTC'), 'y': 0.0},
        {'ds': Timestamp('2021-06-09 00:00:00+0000', tz='UTC'),
        'y': 2.0},
        {'ds': Timestamp('2021-06-10 00:00:00+0000', tz='UTC'),
        'y': 1.0},
        {'ds': Timestamp('2021-06-11 00:00:00+0000', tz='UTC'),
        'y': 1.0},
        {'ds': Timestamp('2021-06-12 00:00:00+0000', tz='UTC'),
        'y': 1.0},
        {'ds': Timestamp('2021-06-13 00:00:00+0000', tz='UTC'),
        'y': 1.0},
        {'ds': Timestamp('2021-06-14 00:00:00+0000', tz='UTC'),
        'y': 2.0},
        {'ds': Timestamp('2021-06-15 00:00:00+0000', tz='UTC'), 'y': 0.0},
        {'ds': Timestamp('2021-06-16 00:00:00+0000', tz='UTC'),
        'y': 2.0},
        {'ds': Timestamp('2021-06-17 00:00:00+0000', tz='UTC'),
        'y': 1.0},
        {'ds': Timestamp('2021-06-18 00:00:00+0000', tz='UTC'),
        'y': 2.0},
        {'ds': Timestamp('2021-06-19 00:00:00+0000', tz='UTC'),
        'y': 1.0},
        {'ds': Timestamp('2021-06-20 00:00:00+0000', tz='UTC'),
        'y': 2.0},
        {'ds': Timestamp('2021-06-21 00:00:00+0000', tz='UTC'),
        'y': 4.0},
        {'ds': Timestamp('2021-06-22 00:00:00+0000', tz='UTC'),
        'y': 3.0},
        {'ds': Timestamp('2021-06-23 00:00:00+0000', tz='UTC'),
        'y': 1.0},
        {'ds': Timestamp('2021-06-24 00:00:00+0000', tz='UTC'), 'y': 0.0},
        {'ds': Timestamp('2021-06-25 00:00:00+0000', tz='UTC'),
        'y': 3.0},
        {'ds': Timestamp('2021-06-26 00:00:00+0000', tz='UTC'),
        'y': 3.0},
        {'ds': Timestamp('2021-06-27 00:00:00+0000', tz='UTC'),
        'y': 1.0},
        {'ds': Timestamp('2021-06-28 00:00:00+0000', tz='UTC'), 'y': 0.0},
        {'ds': Timestamp('2021-06-29 00:00:00+0000', tz='UTC'), 'y': 0.0},
        {'ds': Timestamp('2021-06-30 00:00:00+0000', tz='UTC'), 'y': 0.0}]
    
    dts = mixer.blend("anomaly.Dataset", granularity="day")
    anomDef = mixer.blend("anomaly.AnomalyDefinition", dataset=dts, periodicTask=None)

    dimValObj = {
        "dimVal": "xkcd",
        "anomalyId": 1,
        "contriPercent": 12
    }

    anomalyDefProps = {
        "granularity": "day",
        "highOrLow": ""
    }

    

    result = anomalyService(dimValObj, fakedata, anomalyDefProps, "Prophet", {})
    

    
    assert result["success"]
    assert not result["published"]
