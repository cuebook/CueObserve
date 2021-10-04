import logging

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)


class SlackAlert:
    def cueObserveAnomalyAlert(token, channelId, fileImg, title="", message="", details=""):
        """
        Image uploads in slack
        """
        client = WebClient(token=token)
        try:
            # Call the files.upload method using the WebClient
            # Uploading files requires the `files:write` scope
            result = client.files_upload(
                # ID of channel that you want to upload file to
                channels=channelId,
                # initial_comment="Here's my file :smile:",
                initial_comment=message + "\n" + details,
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
                text="*" + title + "*" + "\n" + message
            )
            logger.info(result)

        except SlackApiError as e:
            logger.error(f"Error posting message: {e}")
