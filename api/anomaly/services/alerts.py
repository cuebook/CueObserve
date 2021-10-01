import logging
from email.mime.image import MIMEImage
import requests
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from anomaly.services.settings import (
    ANOMALY_ALERT_SLACK_ID,
    APP_ALERTS_SLACK_ID,
    SLACK_BOT_TOKEN,
    SEND_EMAIL_TO,
    WEBHOOK_URL,
)
from anomaly.models import Setting
from anomaly.services.plotChart import PlotChartService

logger = logging.getLogger(__name__)


class SlackAlert:
    @staticmethod
    def slackAlertHelper(title, message, name, details="", anomalyId: int = None):
        """
        Helper method for slackAlert
        """
        token = ""
        anomalyAlertChannelId = ""
        appAlertChannelId = ""
        try:
            settings = Setting.objects.all()
            for setting in settings.values():
                if setting["name"] == ANOMALY_ALERT_SLACK_ID:
                    anomalyAlertChannelId = setting["value"]
                elif setting["name"] == APP_ALERTS_SLACK_ID:
                    appAlertChannelId = setting["value"]
                elif setting["name"] == SLACK_BOT_TOKEN:
                    token = setting["value"]
            # Anomaly Detection Alert
            if name == "anomalyAlert":
                SlackAlert.cueObserveAnomalyAlert(
                    token, anomalyAlertChannelId, anomalyId, title, message, details
                )
            # AppAlert
            if name == "appAlert":
                SlackAlert.cueObserveAlert(token, appAlertChannelId, title, message)
        except Exception as ex:
            logger.error("Slack URL not given or wrong URL given:%s", str(ex))

    @staticmethod
    def cueObserveAnomalyAlert(
        token, channelId, anomalyId, title="", message="", details=""
    ):
        """
        Image uploads in slack
        """
        fileImg = PlotChartService.anomalyChartToImgStr(anomalyId)
        client = WebClient(token=token)
        # The name of the file you're going to upload
        fileName = fileImg
        try:
            # Call the files.upload method using the WebClient
            # Uploading files requires the `files:write` scope
            result = client.files_upload(
                # ID of channel that you want to upload file to
                channels=channelId,
                # initial_comment="Here's my file :smile:",
                initial_comment=message + "\n" + details,
                title=title,
                file=fileName,
            )
            # Log the result
            logger.info(result)

        except SlackApiError as e:
            logger.error("Error uploading file: {}".format(e))

    @staticmethod
    def cueObserveAlert(token, channelId, title="", message=""):
        """Post message in slack"""

        client = WebClient(token=token)
        try:
            # Call the chat.postMessage method using the WebClient
            result = client.chat_postMessage(
                channel=channelId, text="*" + title + "*" + "\n" + message
            )
            logger.info(result)
        except SlackApiError as e:
            logger.error(f"Error posting message: {e}")


class EmailAlert:
    @staticmethod
    def sendEmail(message, details, subject, anomalyId):
        """
        Email alert with image
        """
        sendEmailTo = []
        settingObjs = Setting.objects.all()
        for settingObj in settingObjs.values():
            if settingObj["name"] == SEND_EMAIL_TO:
                sendEmailTo = settingObj["value"]
        sendEmailTo = sendEmailTo.split(",")
        try:
            logger.info("Sending email procedure starts")
            imgByte = PlotChartService.anomalyChartToImgStr(anomalyId)
            subject, from_email, to = subject, settings.EMAIL_HOST_USER, sendEmailTo
            body_html = (
                message
                + details
                + """
                <html>
                    <body>
                        <img src="cid:logo.png" alt="anomaly image" />
                    </body>
                </html>
                """
            )
            msg = EmailMultiAlternatives(
                subject, body_html, from_email=from_email, to=to
            )
            msg.mixed_subtype = "related"
            msg.attach_alternative(body_html, "text/html")
            image = "logo.png"
            img = MIMEImage(imgByte)
            img.add_header("Content-ID", "<{name}>".format(name=image))
            img.add_header("Content-Disposition", "inline", filename=image)
            msg.attach(img)
            msg.send()
            logger.info("Email sent successfully !")
        except Exception as ex:
            logger.error(f"Email sent procedure failed ! {ex}")


class WebHookAlert:
    """Generic rest api for alert on webhook URL"""

    @staticmethod
    def webhookAlertHelper(
        name,
        subject,
        message,
        details="",
        anomalyDefId: int = None,
        anomalyId: int = None,
    ):
        try:
            webhookURL = ""
            settings = Setting.objects.all()
            for setting in settings.values():
                if setting["name"] == WEBHOOK_URL:
                    webhookURL = setting["value"]
            if name == "anomalyAlert":
                WebHookAlert.webookAnomalyAlert(
                    webhookURL, message, details, subject, anomalyDefId, anomalyId
                )
            if name == "appAlert":
                WebHookAlert.webookAppAlert(webhookURL, message, subject)
        except Exception as ex:
            logger.error("Webhook URL not given or URL not found:%s", str(ex))

    @staticmethod
    def webookAnomalyAlert(url, message, details, subject, anomalyDefId, anomalyId):
        """Alerts Json formatted message in given Webhook URL, When anomaly is detected on anomaly definition"""
        responseJson = {
            "subject": subject,
            "message": message,
            "details": details,
            "AnomalyDefinitionId": anomalyDefId,
            "AnomalyId": anomalyId,
        }
        try:
            fileImg = PlotChartService.anomalyChartToImgStr(anomalyId)
            response = requests.post(url, data=responseJson, files={"fileImg": fileImg})
            if response.status_code == 200:
                logger.info("Alert sent to the URL :%s", str(url))
        except Exception as ex:
            logger.error(
                "Webhook URL not accepting json data format or Wrong Webhook URL given :%s",
                str(ex),
            )

    @staticmethod
    def webookAppAlert(url, message, subject):
        """Alerts JSON formatted message when anomaly detection job fails"""
        responseJson = {
            "subject": subject,
            "message": message,
        }
        try:
            response = requests.post(url, data=responseJson)
            if response.status_code == 200:
                logger.info("Alert sent to the URL :%s", str(url))

        except Exception as ex:
            logger.error(
                "Webhook URL not accepting json data format or Wrong Webhook URL given :%s",
                str(ex),
            )
