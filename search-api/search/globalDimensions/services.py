from .models import GlobalDimension, GlobalDimensionValues
from search import app, db
from flask import Flask, request, jsonify, make_response
from .serializer import GlobalDimensionSchema, GlobalDimensionValuesSchema
import requests



def createGlobalDimension(payloads):
    """ Create global dimension"""
    app.logger.info("payloads %s", payloads)
    name = payloads["name"]
    globalDimension = GlobalDimension(name=name)
    db.session.add(globalDimension)
    db.session.commit()

    dimensions = payloads["dimensionalValues"]
    objs = payloads["dimensionalValues"]
    dimensionalValueObjs = []
    for obj in objs:
        gdValues = GlobalDimensionValues(datasetId = obj["datasetId"], datasetName = obj["datasetName"], dimensionName = obj["dimension"], globalDimensionId = globalDimension.id)
        dimensionalValueObjs.append(gdValues)
    app.logger.info("dimensionalValuesOBjs %s", dimensionalValueObjs)
    db.session.bulk_save_objects(dimensionalValueObjs)
    db.session.commit()
    res = {"success":True}
    return res

def getDimensionFromCueObserve():
    """ Get dimension from cueObserve"""
    url = "http://localhost:8000/api/anomaly/search/dimension/"
    response = requests.get(url)
        # response = {"success":True}
    app.logger.info("resopnse %s", (response.json()))
    payloads  = response.json()["data"]
    payloadDicts = []
    for payload in payloads:
        for dimension in payload["dimensions"]:
            dictObjs = {}
            dictObjs["datasetName"] = payload["name"]
            dictObjs["datasetId"] = payload["id"]
            dictObjs["dimension"] = dimension
            payloadDicts.append(dictObjs)

    res = payloadDicts
    return res

def getGlobalDimensions():
    """ Services to get Global dimension and their linked dimension"""
    globalDimensions = GlobalDimension.query.all()
    data = GlobalDimensionSchema(many=True).dump(globalDimensions)
    app.logger.info("GLobalDImension in services %s", data)
    
    return data

