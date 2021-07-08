import logging
from typing import List
from utils.apiResponse import ApiResponse
from dbConnections import BigQuery
from anomaly.models import AnomalyDefinition, Dataset
from anomaly.serializers import AnomalyDefinitionSerializer

class AnomalyDefinitions:

    @staticmethod
    def getAllAnomalyDefinition():
        """
        This method is used to get all anomlayObj
        """

        response = ApiResponse("Error in getting Anomaly Definition !")
        anomalyDef = AnomalyDefinition.objects.all().order_by("-id")
        anomalyDefSerializer = AnomalyDefinitionSerializer(anomalyDef, many=True)
        response.update(True, "AnomalyDefinitions retrived successfully !", anomalyDefSerializer.data)

        return response

    @staticmethod
    def addAnomalyDefinition(metric: str = None, dimension: str = None, highOrLow: str = None, top: int = 0, datasetId: int = 0):
        """
        This method is used to add anomaly to AnomalyDefinition table
        """
        response = ApiResponse("Error in creating Anomaly Definition !")
        anomalyObj = AnomalyDefinition.objects.create(
            dataset_id=datasetId,
            metric=metric,
            dimension=dimension,
            highOrLow=highOrLow,
            top=top
        )
        response.update(True, "Anomaly Definition created successfully !")
        return response

    @staticmethod
    def deleteAnomalyDefinition(anomalyId):
        """
        Delete anomaly objects of given id
        """
        response = ApiResponse("Error in creating Anomaly Definition !")
        anomalyObj = AnomalyDefinition.objects.get(id=anomalyId)
        anomalyObj.delete()
        response.update(True,"Anomaly Definition successfully deleted !")
        return response

    @staticmethod
    def editAnomalyDefinition(anomalyId: int = 0, highOrLow: str = None):
        """
        Update anomaly objects of given anomalyId
        """
        response = ApiResponse("Error in updating Anomaly Definition !")
        anomalyObj = AnomalyDefinition.objects.get(id=anomalyId)
        anomalyObj.highOrLow = highOrLow
        anomalyObj.save()
        response.update(True, "Anomaly Definition updated successfully !")
        return response

        

