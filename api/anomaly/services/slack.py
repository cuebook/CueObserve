import os
import json
import sys
import logging
import random
from typing import Set
from celery.utils.log import set_in_sighandler
import requests
from anomaly.models import Anomaly, Setting
from anomaly.services import plotly
from anomaly.services.plotly import Plotly
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)



class SlackAlert:
    # def slackAlert(url, title, message):
    #     url = url
    #     # message = "A Sample Message"
    #     # title = "New Incoming Alert Message "
    #     message = message
    #     title = title
    #     slack_data = {
    #         "username": "CueObserveBot",
    #         "icon_emoji": ":satellite:",
    #         # "channel" : "#cue-observe",
    #         "channel" : "#test",
    #         "attachments": [
    #             {
    #                 "color": "#9733EE",
    #                 "fields": [
    #                     {
    #                         "title": title,
    #                         "value": message,
    #                         "short": "false",
    #                     }
    #                 ]
    #             }
    #         ]
    #     }
    #     byte_length = str(sys.getsizeof(slack_data))
    #     headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    #     response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    #     if response.status_code != 200:
    #         raise Exception(response.status_code, response.text)

    # def slackAnomalyAlert(url, title, message, details):
    #         url = url
    #         # message = "A Sample Message"
    #         # title = "New Incoming Alert Message "
    #         message = message
    #         title = title
    #         slack_data = {
    #             "username": "CueObserveBot",
    #             "icon_emoji": ":satellite:",
    #             # "channel" : "#cue-observe-anomaly",
    #             "channel" : "#test",
    #             "blocks": [
    #                 {
    #                     "type": "section",
    #                     "text": {
    #                         "type": "mrkdwn",
    #                         "text": message
    #                     }
    #                 },
    #                 {
    #                     "type": "divider"
    #                 },
    #                 {
    #                     "type": "section",
    #                     "text": {
    #                         "type": "mrkdwn",
    #                         "text": details
    #                     },
    #                 }
    #             ]
    #         }
    #         byte_length = str(sys.getsizeof(slack_data))
    #         headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    #         response = requests.post(url, data=json.dumps(slack_data), headers=headers)
    #         if response.status_code != 200:
    #             raise Exception(response.status_code, response.text)


    def slackAlertHelper(title, message, name, details="", anomalyId: int = None ):
        """
        Helper method for slackAlert
        """
        token = ''
        channelId = ''
        try:
            setting = Setting.objects.all()
            token = setting.values()[0]["value"]
            # Anomaly Detection successfull 
            if name == "anomalyAlert":
                channelId = setting.values()[1]["value"]
                SlackAlert.cueObserveAnomalyAlert(token, channelId, anomalyId ,title, message, details)
            # Anomaly Detection job failed
            if name == "appAlert":
                channelId = setting.values()[2]["value"]
                SlackAlert.cueObserveAlert(token, channelId, title, message)

        except Exception as ex:
            logger.error("Slack URL not given or wrong URL given:%s", str(ex))


    def cueObserveAnomalyAlert(token, channelId, anomalyId, title="", message="", details=""):
        """
        Image uploads in slack
        """

        fileImg = Plotly.anomalyChartToImgStr(anomalyId)
        client = WebClient(token=token)  
        # The name of the file you're going to upload
        file_name = fileImg
        try:
            # Call the files.upload method using the WebClient
            # Uploading files requires the `files:write` scope
            result = client.files_upload(
            # ID of channel that you want to upload file to
                channels=channelId,
                # initial_comment="Here's my file :smile:",
                initial_comment = message + "\n" + details ,
                title=title,
                file=fileImg,
            )
            # Log the result
            logger.info(result)

        except SlackApiError as e:
            logger.error("Error uploading file: {}".format(e))

    def cueObserveAlert(token, channelId, title="", message=""):
        """ Post message in slack"""

        client = WebClient(token=token)
        try:
            # Call the chat.postMessage method using the WebClient
            result = client.chat_postMessage(
                channel=channelId, 
                text= "*" + title + "*" + "\n" + message 
            )
            logger.info(result)

        except SlackApiError as e:
            logger.error(f"Error posting message: {e}")


