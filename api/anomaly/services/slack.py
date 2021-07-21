import json
import sys
import logging
import random
from typing import Set
from celery.utils.log import set_in_sighandler
import requests
from anomaly.models import Setting
logger = logging.getLogger(__name__)



class SlackAlert:
    def slackAlert(url, title, message):
        url = url
        # message = "A Sample Message"
        # title = "New Incoming Alert Message "
        message = message
        title = title
        slack_data = {
            "username": "CueObserveBot",
            "icon_emoji": ":satellite:",
            "channel" : "#cue-observe",
            "attachments": [
                {
                    "color": "#9733EE",
                    "fields": [
                        {
                            "title": title,
                            "value": message,
                            "short": "false",
                        }
                    ]
                }
            ]
        }
        byte_length = str(sys.getsizeof(slack_data))
        headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
        response = requests.post(url, data=json.dumps(slack_data), headers=headers)
        if response.status_code != 200:
            raise Exception(response.status_code, response.text)

    def slackAnomalyAlert(url, title, message):
            url = url
            # message = "A Sample Message"
            # title = "New Incoming Alert Message "
            message = message
            title = title
            slack_data = {
                "username": "CueObserveBot",
                "icon_emoji": ":satellite:",
                "channel" : "#cue-observe-anomaly",
                "attachments": [
                    {
                        "color": "#9733EE",
                        "fields": [
                            {
                                "title": title,
                                "value": message,
                                "short": "false",
                            }
                        ]
                    }
                ]
            }
            byte_length = str(sys.getsizeof(slack_data))
            headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
            response = requests.post(url, data=json.dumps(slack_data), headers=headers)
            if response.status_code != 200:
                raise Exception(response.status_code, response.text)


    def slackAlertHelper(title, message, name):
        """
        Helper method for slackAlert
        """

        try:
            setting = Setting.objects.all()
            # Anomaly Detection successfull 
            if name == "anomalyAlert":
                url = setting.values()[0]["value"]
                SlackAlert.slackAnomalyAlert(url, title, message)
            # Anomaly Detection job failed
            if name == "appAlert":
                url = setting.values()[1]["value"]
                SlackAlert.slackAlert(url, title, message)

        except Exception as ex:
            logger.error("Slack URL not given or wrong URL given:%s", str(ex))


