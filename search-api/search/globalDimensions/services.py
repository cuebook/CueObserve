# from requests.models import Response
import traceback
from search import app, db
from sqlalchemy import desc
import requests
from .models import GlobalDimension, GlobalDimensionValues
from .serializer import GlobalDimensionSchema
from config import DIMENSION_URL
from elasticSearch import ESIndexingUtils

class GlobalDimensionServices:
    """ Services for Global Dimension """
    def createGlobalDimension(payloads):
        """ Create global dimension"""
        try:
            name = payloads["name"]
            app.logger.info("Create Global Dimension of name %s", name)
            globalDimension = GlobalDimension(name=name)
            db.session.add(globalDimension)
            db.session.flush()
            app.logger.info("Global dimension objs saved ")
            objs = payloads["dimensionalValues"]
            dimensionalValueObjs = []
            for obj in objs:
                gdValues = GlobalDimensionValues(datasetId = obj["datasetId"], dataset = obj["dataset"], dimension = obj["dimension"], globalDimensionId = globalDimension.id)
                dimensionalValueObjs.append(gdValues)
            app.logger.info("dimensionalValuesOBjs %s", dimensionalValueObjs)
            db.session.bulk_save_objects(dimensionalValueObjs)
            db.session.commit()
            app.logger.info("Global Dimension Values created ")
            try:
                app.logger.info("Indexing starts")
                ESIndexingUtils.indexGlobalDimension()
                app.logger.info("Indexing completed")
            except Exception as ex:
                app.logger.error("Indexing Failed %s", ex)

            res = {"success":True}
        except Exception as ex:
            res = {"success":False, "message":"Global Dimension name already exists."}
            app.logger.error("Exception occured: " + str(ex))
            db.session.rollback()
        return res

    def deleteGlobalDimension(id):
        try:
            globalDimension = GlobalDimension.query.get(id)
            db.session.delete(globalDimension)
            db.session.commit()
            res = {"success":True}
            return res
        except Exception as ex:
            app.logger.error("Error occured while delete global dimension of Id : ",id)
            db.session.rollback()
            res = {"success":False, "message": "Error occured while deleting global dimension "}

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
        except Exception as ex:
            app.logger.error*("Failed to get dimension %s", ex)
            res = {"success":False, "data":[], "message":"Error occured to get dimension from cueObserve"}
        return res


    def getGlobalDimensions():
        """ Services to get Global dimension and their linked dimension"""
        try:
            app.logger.info("Get Global Dimension")
            globalDimensions = GlobalDimension.query.order_by(desc(GlobalDimension.id)).all()
            data = GlobalDimensionSchema(many=True).dump(globalDimensions)
            res = {"success":True, "data":data}
        except Exception as ex:
            app.logger.error("Failed to get global dimension %s", ex)
            res = {"success":False, "data":[], "message":"Error occured to get data in global dimension"}
        return res


    def publishGlobalDimension(payload):
        """ Service to publish / unpublish global dimension """
        try:
            published = payload.get("published", False)
            globalDimensionId = payload.get("id", None)
            res = ''
            if globalDimensionId:
                globalDimensionObj = GlobalDimension.query.get(globalDimensionId)
                globalDimensionObj.published = published
                db.session.commit()
                res = {"success":True, "message":"Global Dimension updated successfully"}
            else:
                res = {"success":False, "message": "Id is mandatory"}
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
        except Exception as ex:
            app.logger.error("Failed to get global dimension of id %s", id)
            app.logger.error("Error %s", ex)
            res = {"success":True, "data": [], "message":"Failed to get global dimension of id : " + id }
        return res

    def updateGlobalDimensionById(id, payload):
        try:
            name = payload.get("name", "")
            objs = payload.get("dimensionalValues", [])
            published = payload.get("published", False)
            dimensionalValueObjs = []
            globalDimension = GlobalDimension.query.get(id)
            newId = globalDimension.id
            db.session.delete(globalDimension)
            db.session.flush()
            app.logger.info("flushed global dimension %s", globalDimension)
            gd = GlobalDimension(id=newId, name=name, published=published)
            db.session.add(gd)
            db.session.flush()
            for obj in objs:
                gdValues = GlobalDimensionValues(datasetId = obj["datasetId"], dataset = obj["dataset"], dimension = obj["dimension"], globalDimensionId = gd.id)
                dimensionalValueObjs.append(gdValues)
            db.session.bulk_save_objects(dimensionalValueObjs)
            db.session.commit()
            # Global dimension indexing on Global dimension update
            try:
                ESIndexingUtils.indexGlobalDimension()
                app.logger.info("Indexing completed")
            except Exception as ex:
                app.logger.error("Indexing Failed %s", ex)
            res = {"success":True, "message":"Global Dimension updated successfully"}
        except Exception as ex:
            app.logger.error("Failed to update global dimension of Id : %s", id)
            app.logger.error("Traces of failure %s", ex)
            db.session.rollback()
            res = {"success":False, "message":"Error occured while updating global dimension"}
        return res

