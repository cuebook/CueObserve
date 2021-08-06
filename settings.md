# Settings

## Slack

CueObserve can send two types of Slack alerts:

1. Anomaly alerts are sent when an anomaly is detected
2. App Monitoring alerts are sent when an anomaly detection job fails

To get these alerts, enter your Slack Incoming Webhooks. To create an Incoming Webhook, follow the steps outlined in [Slack documentation](https://api.slack.com/messaging/webhooks).

1. Create a slack app.
2. Once you create the app, you will be redirected to your app’s `Basic Information` screen. In `Add features and functionality`, click on `Incoming Webhooks`.
3. On the next screen, use the slider button to Activate incoming webhooks.
4. Click on `Add New Webhook to Workspace`.
5. In the next screen, choose a channel from your Slack workspace and click `Allow`.
6. You will now be redirected to your app’s incoming webhooks screen, where you'll get your  `Webhook URL`

