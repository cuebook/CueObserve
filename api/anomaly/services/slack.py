import os
import json
import sys
import random
import logging
import requests
from typing import Set
from celery.utils.log import set_in_sighandler
from anomaly.models import Anomaly, Setting
from anomaly.services.plotChart import PlotChartService
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)



class SlackAlert:

    def slackAlertHelper(title, message, name, details="", anomalyId: int = None ):
        """
        Helper method for slackAlert
        """
        token = ''
        channelId = ''
        try:
            setting = Setting.objects.all()
            token = setting.values()[0]["value"]
            # Anomaly Detection Alert 
            if name == "anomalyAlert":
                channelId = setting.values()[1]["value"]
                SlackAlert.cueObserveAnomalyAlert(token, channelId, anomalyId ,title, message, details)
            # AppAlert
            if name == "appAlert":
                channelId = setting.values()[2]["value"]
                SlackAlert.cueObserveAlert(token, channelId, title, message)

        except Exception as ex:
            logger.error("Slack URL not given or wrong URL given:%s", str(ex))


    def cueObserveAnomalyAlert(token, channelId, anomalyId, title="", message="", details=""):
        """
        Image uploads in slack
        """

        fileImg = PlotChartService.anomalyChartToImgStr(anomalyId)
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


