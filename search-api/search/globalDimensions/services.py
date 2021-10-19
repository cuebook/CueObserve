# from requests.models import Response
from search import app, db
from sqlalchemy import desc
from flask import Flask, request, jsonify, make_response
import requests
from .models import GlobalDimension, GlobalDimensionValues
from .serializer import GlobalDimensionSchema, GlobalDimensionValuesSchema
from config import DIMENSION_URL, METRIC_URL
from elasticSearch import ESIndexingUtils

def createGlobalDimension(payloads):
    """ Create global dimension"""
    try:
        name = payloads["name"]
        app.logger.info("Global dimension creating with name %s", name)
        globalDimension = GlobalDimension(name=name)
        db.session.add(globalDimension)
        db.session.flush()
        app.logger.info("Global dimension objs saved ")
        dimensions = payloads["dimensionalValues"]
        objs = payloads["dimensionalValues"]
        dimensionalValueObjs = []
        for obj in objs:
            gdValues = GlobalDimensionValues(datasetId = obj["datasetId"], dataset = obj["dataset"], dimension = obj["dimension"], globalDimensionId = globalDimension.id)
            dimensionalValueObjs.append(gdValues)
        app.logger.info("dimensionalValuesOBjs %s", dimensionalValueObjs)
        db.session.bulk_save_objects(dimensionalValueObjs)
        db.session.flush()
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
        url = DIMENSION_URL
        response = requests.get(url)
        payloads  = response.json().get("data", [])
        payloadDicts = []
        for payload in payloads:
            for dimension in payload.get("dimensions", []):
                dictObjs = {}
                dictObjs["dataset"] = payload["name"]
                dictObjs["datasetId"] = payload["id"]
                dictObjs["dimension"] = dimension
                payloadDicts.append(dictObjs)

        res = {"success":True, "data":payloadDicts}
        return res
    except Exception as ex:
        app.logger.error*("Failed to get dimension %s", ex)
        res = {"success":False, "data":[], "message":"Error occured to get dimension from cueObserve"}



def getGlobalDimensions():
    """ Services to get Global dimension and their linked dimension"""
    try:
        app.logger.info("Get Global Dimension")
        globalDimensions = GlobalDimension.query.order_by(desc(GlobalDimension.id)).all()
        data = GlobalDimensionSchema(many=True).dump(globalDimensions)
        res = {"success":True, "data":data}
        return res

    except Exception as ex:
        app.logger.error("Failed to get global dimension %s", ex)
        res = {"success":False, "data":[], "message":"Error occured to get data in global dimension"}
        return res


def publishGlobalDimension(payload):
    """ Service to publish / unpublish global dimension """
    try:
        published = payload.get("published", False)
        globalDimensionId = payload.get("id", None)
        app.logger.info("published %s", published)
        app.logger.info("id %s", globalDimensionId)
        globalDimensionObj = GlobalDimension.query.get(globalDimensionId)
        db.session.add(globalDimensionObj)
        globalDimensionObj.published = published
        db.session.flush()
        db.session.commit()
        app.logger.info("GlobalDimension object saved")
        res = {"success":True, "message":"Global Dimension updated successfully"}
        return res
    except Exception as ex:
        app.logger.error("Failed to publish/unpublish global dimension %s", ex)
        db.session.rollback()
        res = {"success":False, "message": "Error occured while updating global dimension"}
        return res

def getGlobalDimensionById(id):
    """ Service to get global dimension of given id """
    try:
        globalDimensionObj = GlobalDimension.query.get(id)
        data = GlobalDimensionSchema().dump(globalDimensionObj)
        app.logger.info("data %s", data)
        res = {"success":True, "data": data }
        return res
    except Exception as ex:
        app.logger.error("Failed to get global dimension of id %s", id)
        app.logger.error("Error %s", ex)
        res = {"success":True, "data": [], "message":"Failed to get global dimension of id : " + id }
        return res

def updateGlobalDimensionById(id, payload):
    try:
        app.logger.info("it should working")
        name = payload.get("name", "")
        objs = payload.get("dimensionalValues", [])
        published = payload.get("published", False)
        dimensionalValueObjs = []
        # Delete
        globalDimension = GlobalDimension.query.get(id)
        newId = globalDimension.id
        db.session.delete(globalDimension)
        db.session.flush()
        app.logger.info("flushed globaldiemension %s", globalDimension)
        gd = GlobalDimension(id=newId, name=name, published=published)
        db.session.add(gd)
        db.session.flush()
        app.logger.error("created till here without erro %s", gd)
        for obj in objs:
            gdValues = GlobalDimensionValues(datasetId = obj["datasetId"], dataset = obj["dataset"], dimension = obj["dimension"], globalDimensionId = gd.id)
            dimensionalValueObjs.append(gdValues)
        app.logger.info("dimensionalValuesOBjs %s", dimensionalValueObjs)
        db.session.bulk_save_objects(dimensionalValueObjs)
        db.session.flush()
        db.session.commit()
        # Global dimension indexing on Global dimension update
        try:
            app.logger.info("Indexing starts")
            ESIndexingUtils.indexGlobalDimensionsData()
            app.logger.info("Indexing completed")
        except Exception as ex:
            app.logger.error("Indexing Failed %s", ex)

        res = {"success":True, "message":"Global Dimension updated successfully"}
        return res
    except Exception as ex:
        app.logger.error("Failed to update global dimension of Id : %s", id)
        app.logger.error("Traces of failure %s", ex)
        db.session.rollback()
        res = {"success":False, "message":"Error occured while updating global dimension"}
        return res

