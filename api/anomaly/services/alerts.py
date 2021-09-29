import logging
import os
from email.mime.image import MIMEImage

import requests
from anomaly.models import Setting
from anomaly.services.plotChart import PlotChartService
from anomaly.services.settings import ANOMALY_ALERT_SLACK_ID, APP_ALERTS_SLACK_ID, SEND_EMAIL_TO, SLACK_BOT_TOKEN
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

logger = logging.getLogger(__name__)
ALERT_API_URL = os.environ.get("ALERT_API_URL", "localhost:8100")


class SlackAlert:

    def slackAlertHelper(title, message, name, details="", anomalyId: int = None):
        """
        Helper method for slackAlert
        """
        token = ''
        anomalyAlertChannelId = ''
        appAlertChannelId = ''
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
                url = f'{ALERT_API_URL}/alerts/anamoly-alert'
                payload = {
                    "token": token,
                    "anomalyAlertChannelId": anomalyAlertChannelId,
                    "title": title,
                    "meesage": message,
                    "details": details,
                    "fileImg": PlotChartService.anomalyChartToImgStr(anomalyId)
                }
                requests.request("POST", url, data=payload)
            # AppAlert
            if name == "appAlert":
                url = f'{ALERT_API_URL}/alerts/app-alert'
                payload = {
                    "token": token,
                    "appAlertChannelId": appAlertChannelId,
                    "title": title,
                    "meesage": message
                }
                requests.request("POST", url, data=payload)

        except Exception as ex:
            logger.error("Slack URL not given or wrong URL given:%s", str(ex))


class EmailAlert:

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
            body_html = message + details + '''
                <html>
                    <body>
                        <img src="cid:logo.png" alt="anomaly image" />
                    </body>
                </html>
                '''
            msg = EmailMultiAlternatives(
                subject,
                body_html,
                from_email=from_email,
                to=to
            )
            msg.mixed_subtype = 'related'
            msg.attach_alternative(body_html, "text/html")
            image = 'logo.png'
            img = MIMEImage(imgByte)
            img.add_header('Content-ID', '<{name}>'.format(name=image))
            img.add_header('Content-Disposition', 'inline', filename=image)
            msg.attach(img)
            msg.send()
            logger.info("Email sent successfully !")
        except Exception as ex:
            logger.error(f"Email sent procedure failed ! {ex}")
