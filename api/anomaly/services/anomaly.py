import logging
from typing import List
from utils.apiResponse import ApiResponse
from dbConnections import BigQuery
from anomaly.models import AnomalyDefinition, Dataset
from anomaly.serializers import AnomalyDefinitionSerializer

class Anomalys:

    @staticmethod
    def getAnomalys():
        """
        This method is used to get all anomlayObj
        """

        response = ApiResponse("Error in getting AnomalyObject")
        anomalyDef = AnomalyDefinition.objects.all()
        anomalyDefSerializer = AnomalyDefinitionSerializer(anomalyDef, many=True)
        response.update(True, "AnomalyObj retrived successfully", anomalyDefSerializer.data)

        return response

    @staticmethod
    def addAnomalyObj(metric: str = None, dimension: str = None, highOrLow: str = None, top: int = 0, datasetId: int = 0):
        """
        This method is used to add anomaly to AnomalyDefinition table
        """
        response = ApiResponse("Error in creating AnomalyObject")
        anomalyObj, created = AnomalyDefinition.objects.get_or_create(
            dataset_id=datasetId,
            metric=metric,
            dimension=dimension,
            highOrLow=highOrLow,
            top=top
        )
        if created:
            response.update(True, "AnomalyObject created ")
        else:
            response.update(False, "AnomalyObject allready exists !")

        return response

    @staticmethod
    def deleteAnomalyObj(id):
        """
        Delete anomaly objectsof given id
        """
        response = ApiResponse("Error in creating AnomalyObject")
        anomalyObj = AnomalyDefinition.objects.get(id=id)
        anomalyObj.delete()
        response.update(True,"Anomaly Object successfully deleted")
        return response


        

