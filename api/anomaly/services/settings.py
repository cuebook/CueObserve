import json
from utils.apiResponse import ApiResponse
from anomaly.models import Setting
from anomaly.serializers import SettingSerializer
from anomaly.settingDetails import settingDicts

ANOMALY_ALERT_SLACK_ID = "Slack Channel ID for Anomaly Alerts"
APP_ALERTS_SLACK_ID= "Slack Channel ID for App Monitoring"
SLACK_BOT_TOKEN = "Bot User OAuth Access Token"
SEND_EMAIL_TO = "Send Email To"
WEBHOOK_URL = "Webhook URL"


class Settings:
    """
    Services for settings
    """
    # defaultSettings: list = [SLACK_BOT_TOKEN, ANOMALY_ALERT_SLACK_ID, APP_ALERTS_SLACK_ID]
    settingObjs = settingDicts()
    defaultSettings: list = []

    for settingObj in settingObjs:
        defaultSettings.append(settingObj["name"])

    @staticmethod
    def getSettings():
        """
        Gets settings
        """
        res = ApiResponse()
        try:
            Settings.__createDefaultSettings()
            data = SettingSerializer(
                Setting.objects.filter(name__in=Settings.defaultSettings).order_by("id"), many=True
            ).data
            res.update(True, "Successfully retrieved settings", data)
        except Exception as ex:
            res.update(False, "Error in retrieving settings")
        return res

    @staticmethod
    def __createDefaultSettings():
        """
        Creates default settings with empty values if not existing
        """
        if (
            len(Settings.defaultSettings)
            == Setting.objects.filter(name__in=Settings.defaultSettings).count()
        ):
            return

        for name in Settings.defaultSettings:
            Setting.objects.update_or_create(name=name, value="")

    @staticmethod
    def updateSettings(payload: dict):
        """
        Update Settings
        :param payload: dict of name value pair
        """
        res = ApiResponse()
        try:
            for name, value in payload.items():
                Setting.objects.filter(name=name).update(value=value)
            res.update(
                True,
                "Successfully updated settings",
            )
        except Exception as ex:
            res.update(False, "Error in updating settings")
        return res
