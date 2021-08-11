from utils.apiResponse import ApiResponse
from anomaly.models import Setting
from anomaly.serializers import SettingSerializer

ANOMALY_ALERT_SLACK_URL = "Slack Webhook URL for Anomaly Alerts"
APP_ALERTS_SLACK_URL = "Slack Webhook URL for App Monitoring"


class Settings:
    """
    Services for settings
    """

    @staticmethod
    def getSettings():
        """
        Gets settings
        """
        res = ApiResponse()
        try:
            Settings.__createDefaultSettings()
            data = SettingSerializer(Setting.objects.all(), many=True).data
            res.update(True, "Successfully retrieved settings", data)
        except Exception as ex:
            res.update(False, "Error in retrieving settings")
        return res

    @staticmethod
    def __createDefaultSettings():
        """
        Creates default settings with empty values if not existing
        """
        defaultSettings: list = [ANOMALY_ALERT_SLACK_URL, APP_ALERTS_SLACK_URL]
        if len(defaultSettings) == Setting.objects.filter(name__in=defaultSettings).count():
            return

        for name in defaultSettings:
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
            res.update(True, "Successfully updated settings", )
        except Exception as ex:
            res.update(False, "Error in updating settings")
        return res


