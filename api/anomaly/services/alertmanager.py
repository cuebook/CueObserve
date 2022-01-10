
import requests


class AlertManagers:

    def cueObserveAlerts(name, message):

        url = "http://localhost:9093/api/v1/alerts"
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

        url = "http://localhost:9093/api/v1/alerts"
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