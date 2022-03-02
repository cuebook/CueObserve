
import requests
import os


ALERTMANAGER_API_URL = os.environ.get("ALERTMANAGER_API_URL", "http://localhost:9093")

class AlertManagers:

    def cueObserveAlerts(name, message):

        url = f'{ALERTMANAGER_API_URL}/api/v1/alerts'
        data = [
                    {
                        "status": "firing",
                        "labels": {
                        "alertname": "CueObserve Alert",
                        "service": name,
                        "severity": "critical",
                        "instance": "1"
                        },
                        "annotations": {
                        "title":"CueObserve Alert",
                        "summary": "Error",
                        "description": message,
                        },
                        "generatorURL": "",
                    }
                ]
        requests.request("POST", url ,json=data)

    def anomalyAlert(name, message, details,subject):

        url = f'{ALERTMANAGER_API_URL}/api/v1/alerts'
        data = [
                    {
                        "status": "firing",
                        "labels": {
                        "alertname": "Anomaly Alert",
                        "service": name,
                        "severity": "critical",
                        "instance": "1"
                        },
                        "annotations": {
                        "title":"Anomaly Alert",
                        "summary": subject,
                        "description": message+" "+details
                        },
                        "generatorURL": "",
                    }
                ]
            
        requests.request("POST", url ,json=data)