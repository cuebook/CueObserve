import json
from core.anomalyDetection import anomalyService

def aws_lambda_handler(event, context):
    """
    AWS Lambda handler function to run anomaly detection service
    """
    payload = json.loads(event["body"])

    dimValObj = payload["dimValObj"]
    dfDict = payload["dfDict"]
    anomalyDefProps = payload["anomalyDefProps"]
    detectionRuleType = payload["detectionRuleType"]
    detectionParams = payload["detectionParams"]

    anomalyServiceResult = anomalyService(
        dimValObj, dfDict, anomalyDefProps, detectionRuleType, detectionParams
    )

    print(f"Returning response: {anomalyServiceResult}")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(anomalyServiceResult)
    }
    