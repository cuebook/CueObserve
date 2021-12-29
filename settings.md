# Settings

## Slack

CueObserve can send two types of Slack alerts:

1. Anomaly alerts are sent when an anomaly is detected
2. App Monitoring alerts are sent when an anomaly detection job fails

To get these alerts, enter your Slack Bot User OAuth Access Token. To create a Slack Bot User OAuth Access Token, follow the steps outlined in [Slack documentation](https://api.slack.com/messaging/webhooks).

1. Create a slack app.
2. Once you create the app, you will be redirected to your app’s `Basic Information` screen. In `Add features and functionality`, click on `Bots`.
3. On the next screen, click on `add a scope` and you will be redirected to OAuth & Permissions page.
4. On the next screen, go to Scopes section, click on `Add on OAuth Scope` and  add `files:write` and `chat:write` permissions, now click on `Install to Workspace` to create the `Bot User OAuth Token` .
5. Copy `Bot User OAuth Token` and paste it in the CueObserve Settings screen.

Next, create two channels in Slack. Add the app to these two channels.&#x20;

1. To find your Slack channel's ID, right-click the channel in Slack and then click on `Open channel details` . You'll find the channel ID at the bottom. Copy and paste it in the CueObserve Settings screen.
2. Click on the `Save` button.

## Email

1. Make sure you have enabled email alert while installation.
2. Add email Id to `Send Email To` input field, If you have to add more than one email Id, make it comma separated in input field as shown below.

![](<.gitbook/assets/Screenshot from 2021-08-26 17-52-09.png>)

## Webhook URL

CueObserve supports Webhook URL for receiving alert messages. There are two type of alerts :

1.  Anomaly alerts, which are sent when an anomaly is detected in data. The response will have json data (as below) and _base64_ encoded image.



    ```
    {
      "subject": subject,
      "message": message,
      "details": details,
      "AnomalyDefinitionId": anomalyDefId,
      "AnomalyId": anomalyId,
    }
    ```
2.  App Monitoring alerts, which are sent when an anomaly detection job fails. The response will have json data as formatted:



    ```
    {
      "subject": subject,
      "message": message
    }
    ```

To subscribe to these alerts, configure your Webhook URL in CueObserve _settings screen_.
