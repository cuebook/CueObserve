from .models import GlobalDimension, GlobalDimensionValues
from search import app


def getGlobalDimensions(payloads):
    """
    Gets all dimensions
    """
    app.logger.info("payloads %s", payloads)
    payloadDicts = []
    for payload in payloads:
        for dimension in payload["dimensions"]:
            dictObjs = {}
            dictObjs["datasetName"] = payload["name"]
            dictObjs["datasetId"] = payload["id"]
            dictObjs["dimension"] = dimension
            payloadDicts.append(dictObjs)


    app.logger.info("payload dicts %s", payloadDicts)
    app.logger.info("payload dicts count %s", len(payloadDicts))
    return payloadDicts

def createGlobalDimension(payloads):
    """ Create global dimension"""
    app.logger.info("payloads %s", payloads)
    name = payloads["name"]
    dimensions = payloads["dimensionalValues"]
    globalDimension = GlobalDimension.query.create(name=name)



    return {"success":"true"}
