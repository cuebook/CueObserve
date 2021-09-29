#!/usr/bin/env python
from flask import Flask, request, jsonify
from .alerts import SlackAlert
app = Flask(__name__)


@app.route('/alerts/anamoly-alert', methods=['POST'])
def anamoly_alert_api():
    data = request.json
    token = data['token']
    anomalyAlertChannelId = data['anomalyAlertChannelId']
    fileImg = data['fileImg']
    title = data['title']
    message = data['message']
    details = data['details']
    SlackAlert.cueObserveAnomalyAlert(token, anomalyAlertChannelId, fileImg, title, message, details)
    return jsonify({"success": True})


@app.route('/alerts/app-alert', methods=['POST'])
def app_alert_api():
    data = request.json
    token = data['token']
    appAlertChannelId = data['anomalyAlertChannelId']
    title = data['title']
    message = data['message']
    SlackAlert.cueObserveAlert(token, appAlertChannelId, title, message)
    return jsonify({"success": True})
