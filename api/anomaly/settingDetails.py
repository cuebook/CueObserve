
def settingDicts():
    """ This dicts is used to make settings form"""
    dicts =   [
            {
            "id": 1,
                "name": "Bot User OAuth Access Token",
                "isEncrypted": False,
                "properties": {
                "rules": [
                    {
                    "required": False,
                    "message": ""
                    }
                ],
                "type": "text",
                }
            },
            {
            "id": 2,
                "name": "Slack Channel ID for Anomaly Alerts",
                "isEncrypted": False,
                "properties": {
                "rules": [
                    {
                    "required": False,
                    "message": ""
                    }
                ],
                "type": "text",
                }
            },

            {
            "id": 3,
                "name": "Slack Channel ID for App Monitoring",
                "isEncrypted": False,
                "properties": {
                "rules": [
                    {
                    "required": False,
                    "message": ""
                    }
                ],
                "type": "text",
                }
            },
            {
            "id": 4,
                "name": "Send Email To",
                "isEncrypted": False,
                "properties": {
                "rules": [
                    {
                    "required": False,
                    "message": ""
                    }
                ],
                "type": "textarea",
                }
            },
            {
            "id": 5,
                "name": "Webhook URL",
                "isEncrypted": False,
                "properties": {
                "rules": [
                    {
                    "required": False,
                    "message": ""
                    }
                ],
                "type": "text",
                }
            }
        ]
    return dicts