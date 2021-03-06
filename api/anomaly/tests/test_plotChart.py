from anomaly.services.alerts import EmailAlert
import pytest
import unittest
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from mixer.backend.django import mixer
from anomaly.services import PlotChartService
from anomaly.services import SlackAlert
from ops.tasks.anomalyDetectionTasks import webhookAlertMessageFormat

@pytest.mark.django_db(transaction=True)
def test_plotChart():
    """" Test case for anomaly chart to img  """
    data = {'anomalyData': {'band': [{'y': [112.14571558223184, 406.80678382251216],
            'ds': '2021-07-06T00:00:00'},
        {'y': [101.59452843937035, 415.30903819248624],
            'ds': '2021-07-07T00:00:00'},
        {'y': [99.09197855972316, 397.8448943803296], 'ds': '2021-07-08T00:00:00'},
        {'y': [103.07256450761703, 396.528057654929], 'ds': '2021-07-09T00:00:00'},
        {'y': [107.0533256956056, 397.72975465500906], 'ds': '2021-07-10T00:00:00'},
        {'y': [77.57614107306414, 384.6050672250078], 'ds': '2021-07-11T00:00:00'},
        {'y': [102.96972148899701, 401.85721448649736],
            'ds': '2021-07-12T00:00:00'},
        {'y': [109.55022056830919, 416.6361624006297], 'ds': '2021-07-13T00:00:00'},
        {'y': [119.64574847876679, 411.2272975899635], 'ds': '2021-07-14T00:00:00'},
        {'y': [102.97723494270647, 384.49100214412493],
            'ds': '2021-07-15T00:00:00'},
        {'y': [84.26429674900523, 401.22571752956725], 'ds': '2021-07-16T00:00:00'},
        {'y': [108.59250600505123, 415.28706126640435],
            'ds': '2021-07-17T00:00:00'},
        {'y': [87.10946223303065, 386.1435989715214], 'ds': '2021-07-18T00:00:00'},
        {'y': [93.70662664739979, 404.6766660689211], 'ds': '2021-07-19T00:00:00'},
        {'y': [114.95527511071369, 420.0050054813228], 'ds': '2021-07-20T00:00:00'},
        {'y': [120.35167459933743, 426.7906773310983], 'ds': '2021-07-21T00:00:00'},
        {'y': [94.84702883491994, 399.87353610853], 'ds': '2021-07-22T00:00:00'},
        {'y': [97.12374511854422, 398.2210224622063], 'ds': '2021-07-23T00:00:00'},
        {'y': [109.24979070936604, 400.37498241040095],
            'ds': '2021-07-24T00:00:00'},
        {'y': [84.16563990480198, 385.7699647123075], 'ds': '2021-07-25T00:00:00'},
        {'y': [96.78590996051686, 396.5364656515311], 'ds': '2021-07-26T00:00:00'},
        {'y': [138.42412241644845, 438.0469149815599], 'ds': '2021-07-27T00:00:00'},
        {'y': [120.28399523833775, 429.0061311026071], 'ds': '2021-07-28T00:00:00'},
        {'y': [97.73033719500846, 408.73492374943373], 'ds': '2021-07-29T00:00:00'},
        {'y': [109.02932730886141, 403.74293485606194],
            'ds': '2021-07-30T00:00:00'},
        {'y': [115.40621823292877, 410.16699824393345],
            'ds': '2021-07-31T00:00:00'},
        {'y': [89.27278512606237, 386.72241819862575], 'ds': '2021-08-01T00:00:00'},
        {'y': [102.79064035364863, 393.94674499816017],
            'ds': '2021-08-02T00:00:00'},
        {'y': [123.53180461315603, 424.138686602635], 'ds': '2021-08-03T00:00:00'},
        {'y': [133.02380475969727, 425.0025982334881], 'ds': '2021-08-04T00:00:00'},
        {'y': [108.78237526742646, 413.11487795278856],
            'ds': '2021-08-05T00:00:00'},
        {'y': [108.39498582477913, 415.26518545922784],
            'ds': '2021-08-06T00:00:00'},
        {'y': [116.76125894606477, 413.98022225996516],
            'ds': '2021-08-07T00:00:00'},
        {'y': [95.38344976186815, 400.73155289778754], 'ds': '2021-08-08T00:00:00'},
        {'y': [112.2325224788485, 408.93852004858877], 'ds': '2021-08-09T00:00:00'},
        {'y': [132.8416128227054, 430.2450754907103], 'ds': '2021-08-10T00:00:00'},
        {'y': [124.9938989881436, 424.40584388047307], 'ds': '2021-08-11T00:00:00'},
        {'y': [116.9490745259896, 410.40523071487064], 'ds': '2021-08-12T00:00:00'},
        {'y': [118.50553320547135, 419.50689975529696],
            'ds': '2021-08-13T00:00:00'},
        {'y': [115.43352915177258, 415.0455897440894], 'ds': '2021-08-14T00:00:00'},
        {'y': [96.05437084301622, 403.95988371251906], 'ds': '2021-08-15T00:00:00'},
        {'y': [122.71591224244114, 401.7165312409063], 'ds': '2021-08-16T00:00:00'},
        {'y': [142.0778547792386, 439.551852955957], 'ds': '2021-08-17T00:00:00'},
        {'y': [143.36351096284423, 437.84323788274435],
            'ds': '2021-08-18T00:00:00'},
        {'y': [123.04049618309402, 415.9991752174786], 'ds': '2021-08-19T00:00:00'},
        {'y': [122.38821591556535, 428.08102308208277],
            'ds': '2021-08-20T00:00:00'},
        {'y': [132.55867544717273, 432.8477424623239], 'ds': '2021-08-21T00:00:00'},
        {'y': [114.09632908924, 401.82904965665523], 'ds': '2021-08-22T00:00:00'},
        {'y': [119.83349051546942, 415.54981863388446],
            'ds': '2021-08-23T00:00:00'},
        {'y': [136.7521916946971, 436.66995548955344], 'ds': '2021-08-24T00:00:00'},
        {'y': [146.734666193552, 451.2572302357844], 'ds': '2021-08-25T00:00:00'},
        {'y': [126.5876891124561, 421.4184379230584], 'ds': '2021-08-26T00:00:00'},
        {'y': [125.53660663617323, 414.30484130769037],
            'ds': '2021-08-27T00:00:00'},
        {'y': [137.6199391942816, 422.1773635994159], 'ds': '2021-08-28T00:00:00'},
        {'y': [115.10743055476095, 415.69106564135257],
            'ds': '2021-08-29T00:00:00'},
        {'y': [128.24541150738014, 423.1659119979813], 'ds': '2021-08-30T00:00:00'},
        {'y': [137.29336544173293, 453.12653665354367],
            'ds': '2021-08-31T00:00:00'},
        {'y': [150.37020359403277, 434.3842794464628], 'ds': '2021-09-01T00:00:00'},
        {'y': [122.04668581557415, 438.3669537377912], 'ds': '2021-09-02T00:00:00'},
        {'y': [128.1660940353566, 427.79854112339194],
            'ds': '2021-09-03T00:00:00'}],
        'actual': [{'y': 145, 'ds': '2021-07-06T00:00:00', 'anomaly': 1},
        {'y': 180, 'ds': '2021-07-07T00:00:00', 'anomaly': 1},
        {'y': 198, 'ds': '2021-07-08T00:00:00', 'anomaly': 1},
        {'y': 145, 'ds': '2021-07-09T00:00:00', 'anomaly': 1},
        {'y': 202, 'ds': '2021-07-10T00:00:00', 'anomaly': 1},
        {'y': 123, 'ds': '2021-07-11T00:00:00', 'anomaly': 1},
        {'y': 143, 'ds': '2021-07-12T00:00:00', 'anomaly': 1},
        {'y': 214, 'ds': '2021-07-13T00:00:00', 'anomaly': 1},
        {'y': 160, 'ds': '2021-07-14T00:00:00', 'anomaly': 1},
        {'y': 142, 'ds': '2021-07-15T00:00:00', 'anomaly': 1},
        {'y': 190, 'ds': '2021-07-16T00:00:00', 'anomaly': 1},
        {'y': 169, 'ds': '2021-07-17T00:00:00', 'anomaly': 1},
        {'y': 124, 'ds': '2021-07-18T00:00:00', 'anomaly': 1},
        {'y': 124, 'ds': '2021-07-19T00:00:00', 'anomaly': 1},
        {'y': 150, 'ds': '2021-07-20T00:00:00', 'anomaly': 1},
        {'y': 162, 'ds': '2021-07-21T00:00:00', 'anomaly': 1},
        {'y': 154, 'ds': '2021-07-22T00:00:00', 'anomaly': 1},
        {'y': 153, 'ds': '2021-07-23T00:00:00', 'anomaly': 1},
        {'y': 157, 'ds': '2021-07-24T00:00:00', 'anomaly': 1},
        {'y': 199, 'ds': '2021-07-25T00:00:00', 'anomaly': 1},
        {'y': 146, 'ds': '2021-07-26T00:00:00', 'anomaly': 1},
        {'y': 184, 'ds': '2021-07-27T00:00:00', 'anomaly': 1},
        {'y': 200, 'ds': '2021-07-28T00:00:00', 'anomaly': 1},
        {'y': 190, 'ds': '2021-07-29T00:00:00', 'anomaly': 1},
        {'y': 199, 'ds': '2021-07-30T00:00:00', 'anomaly': 1},
        {'y': 187, 'ds': '2021-07-31T00:00:00', 'anomaly': 1},
        {'y': 70, 'ds': '2021-08-01T00:00:00', 'anomaly': 15},
        {'y': 247, 'ds': '2021-08-02T00:00:00', 'anomaly': 1},
        {'y': 219, 'ds': '2021-08-03T00:00:00', 'anomaly': 1},
        {'y': 290, 'ds': '2021-08-04T00:00:00', 'anomaly': 1},
        {'y': 193, 'ds': '2021-08-05T00:00:00', 'anomaly': 1},
        {'y': 319, 'ds': '2021-08-06T00:00:00', 'anomaly': 1},
        {'y': 274, 'ds': '2021-08-07T00:00:00', 'anomaly': 1},
        {'y': 273, 'ds': '2021-08-08T00:00:00', 'anomaly': 1},
        {'y': 312, 'ds': '2021-08-09T00:00:00', 'anomaly': 1},
        {'y': 472, 'ds': '2021-08-10T00:00:00', 'anomaly': 15},
        {'y': 368, 'ds': '2021-08-11T00:00:00', 'anomaly': 1},
        {'y': 568, 'ds': '2021-08-12T00:00:00', 'anomaly': 15},
        {'y': 584, 'ds': '2021-08-13T00:00:00', 'anomaly': 15},
        {'y': 930, 'ds': '2021-08-14T00:00:00', 'anomaly': 15},
        {'y': 984, 'ds': '2021-08-15T00:00:00', 'anomaly': 15},
        {'y': 990, 'ds': '2021-08-16T00:00:00', 'anomaly': 15},
        {'y': 1437, 'ds': '2021-08-17T00:00:00', 'anomaly': 15},
        {'y': 1789, 'ds': '2021-08-18T00:00:00', 'anomaly': 15},
        {'y': 509, 'ds': '2021-08-19T00:00:00', 'anomaly': 15}],
        'predicted': [{'y': 509, 'ds': '2021-08-19T00:00:00'},
        {'y': 271, 'ds': '2021-08-20T00:00:00'},
        {'y': 276, 'ds': '2021-08-21T00:00:00'},
        {'y': 255, 'ds': '2021-08-22T00:00:00'},
        {'y': 268, 'ds': '2021-08-23T00:00:00'},
        {'y': 294, 'ds': '2021-08-24T00:00:00'},
        {'y': 295, 'ds': '2021-08-25T00:00:00'},
        {'y': 274, 'ds': '2021-08-26T00:00:00'},
        {'y': 276, 'ds': '2021-08-27T00:00:00'},
        {'y': 281, 'ds': '2021-08-28T00:00:00'},
        {'y': 259, 'ds': '2021-08-29T00:00:00'},
        {'y': 273, 'ds': '2021-08-30T00:00:00'},
        {'y': 298, 'ds': '2021-08-31T00:00:00'},
        {'y': 300, 'ds': '2021-09-01T00:00:00'},
        {'y': 279, 'ds': '2021-09-02T00:00:00'},
        {'y': 281, 'ds': '2021-09-03T00:00:00'}]},
        'contribution': 9.25,
        'anomalyLatest': {'value': 509.0,
        'percent': 22,
        'highOrLow': 'high',
        'anomalyTime': 1629331200000.0,
        'contribution': 9.25,
        'anomalyTimeISO': '2021-08-19T00:00:00'}}
    dts = mixer.blend("anomaly.Dataset", granularity="day")
    adf = mixer.blend("anomaly.AnomalyDefinition", dataset=dts, periodicTask=None)
    anomaly = mixer.blend("anomaly.anomaly", anomalyDefinition=adf,data = data, lastRun=None)
    setting = mixer.blend("anomaly.setting", name="Send Email To", value="admin@domain.com")
    setting1 = mixer.blend("anomaly.setting", name="Webhook URL", value="https://www.google.com/")
    anomalyTemplate = mixer.blend("anomaly.AnomalyCardTemplate", templateName = "Anomaly Daily Template Prophet", title="test", bodyText = "Test")
    img_str = PlotChartService.anomalyChartToImgStr(anomaly.id)
    message = "Hi there !"
    details = "Email alert on anomaly detection "
    subject = "Email alert"
    EmailAlert.sendEmail(message, details, subject, anomaly.id)
    numPublished = 4 # Random number
    webhookAlertMessageFormat(numPublished, adf)
    assert len(img_str) > 0

    data1 = {'anomalyData': {
        'actual': [{'y': 145, 'ds': '2021-07-06T00:00:00', 'anomaly': 1},
        {'y': 180, 'ds': '2021-07-07T00:00:00', 'anomaly': 1},
        {'y': 198, 'ds': '2021-07-08T00:00:00', 'anomaly': 1},
        {'y': 145, 'ds': '2021-07-09T00:00:00', 'anomaly': 1},
        {'y': 202, 'ds': '2021-07-10T00:00:00', 'anomaly': 1},
        {'y': 123, 'ds': '2021-07-11T00:00:00', 'anomaly': 1},
        {'y': 143, 'ds': '2021-07-12T00:00:00', 'anomaly': 1},
        {'y': 214, 'ds': '2021-07-13T00:00:00', 'anomaly': 1},
        {'y': 160, 'ds': '2021-07-14T00:00:00', 'anomaly': 1},
        {'y': 142, 'ds': '2021-07-15T00:00:00', 'anomaly': 1},
        {'y': 190, 'ds': '2021-07-16T00:00:00', 'anomaly': 1},
        {'y': 169, 'ds': '2021-07-17T00:00:00', 'anomaly': 1},
        {'y': 124, 'ds': '2021-07-18T00:00:00', 'anomaly': 1},
        {'y': 124, 'ds': '2021-07-19T00:00:00', 'anomaly': 1},
        {'y': 150, 'ds': '2021-07-20T00:00:00', 'anomaly': 1},
        {'y': 162, 'ds': '2021-07-21T00:00:00', 'anomaly': 1},
        {'y': 154, 'ds': '2021-07-22T00:00:00', 'anomaly': 1},
        {'y': 153, 'ds': '2021-07-23T00:00:00', 'anomaly': 1},
        {'y': 157, 'ds': '2021-07-24T00:00:00', 'anomaly': 1},
        {'y': 199, 'ds': '2021-07-25T00:00:00', 'anomaly': 1},
        {'y': 146, 'ds': '2021-07-26T00:00:00', 'anomaly': 1},
        {'y': 184, 'ds': '2021-07-27T00:00:00', 'anomaly': 1},
        {'y': 200, 'ds': '2021-07-28T00:00:00', 'anomaly': 1},
        {'y': 190, 'ds': '2021-07-29T00:00:00', 'anomaly': 1},
        {'y': 199, 'ds': '2021-07-30T00:00:00', 'anomaly': 1},
        {'y': 187, 'ds': '2021-07-31T00:00:00', 'anomaly': 1},
        {'y': 70, 'ds': '2021-08-01T00:00:00', 'anomaly': 15},
        {'y': 247, 'ds': '2021-08-02T00:00:00', 'anomaly': 1},
        {'y': 219, 'ds': '2021-08-03T00:00:00', 'anomaly': 1},
        {'y': 290, 'ds': '2021-08-04T00:00:00', 'anomaly': 1},
        {'y': 193, 'ds': '2021-08-05T00:00:00', 'anomaly': 1},
        {'y': 319, 'ds': '2021-08-06T00:00:00', 'anomaly': 1},
        {'y': 274, 'ds': '2021-08-07T00:00:00', 'anomaly': 1},
        {'y': 273, 'ds': '2021-08-08T00:00:00', 'anomaly': 1},
        {'y': 312, 'ds': '2021-08-09T00:00:00', 'anomaly': 1},
        {'y': 472, 'ds': '2021-08-10T00:00:00', 'anomaly': 15},
        {'y': 368, 'ds': '2021-08-11T00:00:00', 'anomaly': 1},
        {'y': 568, 'ds': '2021-08-12T00:00:00', 'anomaly': 15},
        {'y': 584, 'ds': '2021-08-13T00:00:00', 'anomaly': 15},
        {'y': 930, 'ds': '2021-08-14T00:00:00', 'anomaly': 15},
        {'y': 984, 'ds': '2021-08-15T00:00:00', 'anomaly': 15},
        {'y': 990, 'ds': '2021-08-16T00:00:00', 'anomaly': 15},
        {'y': 1437, 'ds': '2021-08-17T00:00:00', 'anomaly': 15},
        {'y': 1789, 'ds': '2021-08-18T00:00:00', 'anomaly': 15},
        {'y': 509, 'ds': '2021-08-19T00:00:00', 'anomaly': 15}],
        },
        'contribution': 9.25,
        'anomalyLatest': {'value': 509.0,
        'percent': 22,
        'highOrLow': 'high',
        'anomalyTime': 1629331200000.0,
        'contribution': 9.25,
        'anomalyTimeISO': '2021-08-19T00:00:00'}}
    anomaly1 = mixer.blend("anomaly.anomaly", anomalyDefinition=adf,data = data1, lastRun=None)

    anomalyTemplate1 = mixer.blend("anomaly.AnomalyCardTemplate", templateName = "Anomaly Hourly Template Lifetime", title="test", bodyText = "Test")
    img_str1 = PlotChartService.anomalyChartToImgStr(anomaly1.id)
    message = "Hi there !"
    details = "Email alert on anomaly detection "
    subject = "Email alert"
    EmailAlert.sendEmail(message, details, subject, anomaly1.id)
    numPublished = 4 # Random number
    webhookAlertMessageFormat(numPublished, adf)
    assert len(img_str1) > 0







