from search import app, db
from flask import Flask, request, jsonify, make_response
import requests
from .models import GlobalDimension, GlobalDimensionValues
from .serializer import GlobalDimensionSchema, GlobalDimensionValuesSchema
from config import GET_DIMENSION_URL

def createGlobalDimension(payloads):
    """ Create global dimension"""
    try:
        name = payloads["name"]
        app.logger.info("Global dimension creating with name %s", name)
        globalDimension = GlobalDimension(name=name)
        db.session.add(globalDimension)
        db.session.commit()
        app.logger.info("Global dimension objs saved ")
        dimensions = payloads["dimensionalValues"]
        objs = payloads["dimensionalValues"]
        dimensionalValueObjs = []
        for obj in objs:
            gdValues = GlobalDimensionValues(datasetId = obj["datasetId"], dataset = obj["dataset"], dimension = obj["dimension"], globalDimensionId = globalDimension.id)
            dimensionalValueObjs.append(gdValues)
        app.logger.info("dimensionalValuesOBjs %s", dimensionalValueObjs)
        db.session.bulk_save_objects(dimensionalValueObjs)
        db.session.commit()
        app.logger.info("Global Dimension Values created ")
        res = {"success":True}
        return res
    except Exception as ex:
        res = {"success":False, "message":"Global Dimension name already exists "}
        db.session.rollback()
        return res


def getDimensionFromCueObserve():
    """ Get dimension from cueObserve"""
    try:
        url = GET_DIMENSION_URL
        response = requests.get(url)
        payloads  = response.json()["data"]
        payloadDicts = []
        for payload in payloads:
            for dimension in payload["dimensions"]:
                dictObjs = {}
                dictObjs["dataset"] = payload["name"]
                dictObjs["datasetId"] = payload["id"]
                dictObjs["dimension"] = dimension
                payloadDicts.append(dictObjs)

        res = payloadDicts
        return res

    except Exception as ex:
        app.logger.error*("Failed to get dimension %s", ex)
        return []


def getGlobalDimensions():
    """ Services to get Global dimension and their linked dimension"""
    try:
        app.logger.info("Get Global Dimension")
        globalDimensions = GlobalDimension.query.all()
        data = GlobalDimensionSchema(many=True).dump(globalDimensions)
        return data

    except Exception as ex:
        app.logger.error("Failed to get global dimension %s", ex)
        return []

    

