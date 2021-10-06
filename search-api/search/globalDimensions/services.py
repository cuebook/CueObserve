from .models import GlobalDimension, GlobalDimensionValues
from search import app, db
from flask import Flask, request, jsonify, make_response
import requests

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
    # dimensions = payloads["dimensionalValues"]
    globalDimension = GlobalDimension(name=name)
    db.session.add(globalDimension)
    db.session.commit()
    app.logger.info("globaldimension %s", globalDimension)
    res = {"success":True}
    return res

def getDimensionFromCueObserve():
    """ Get dimension from cueObserve"""
    url = "http://localhost:8000/api/anomaly/search/dimension/"
    response = requests.get(url)
        # response = {"success":True}
    app.logger.info("resopnse %s", (response.json()))
    payloads  = response.json()["data"]
    res = getGlobalDimensions(payloads)
    return res

