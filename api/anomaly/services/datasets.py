from utils.apiResponse import ApiResponse
from anomaly.models import Dataset
from anomaly.serializers import DatasetsSerializer, DatasetSerializer


class Datasets:
    """
    Provides services related to dataset
    """

    @staticmethod
    def getDatasets():
        """
        Gets all datasets
        """
        res = ApiResponse("Error in getting datasets")
        datasets = Dataset.objects.all()
        data = DatasetsSerializer(datasets, many=True).data
        res.update(True, "Successfully retrieved datasets", data)
        return res

    @staticmethod
    def getDataset(datasetId: int):
        """
        Gets a dataset
        :param datasetId: id of a dataset
        """
        res = ApiResponse("Error in getting dataset")
        dataset = Dataset.objects.get(id=datasetId)
        data = DatasetSerializer(dataset).data
        res.update(True, "Successfully retrieved dataset", data)
        return res

    @staticmethod
    def updateDataset(datasetId: int, data: dict):
        """
        Updates a dataset
        :param datasetId: id of dataset
        :param data: contains new name and sql for dataset
        """
        res = ApiResponse("Error in updating dataset")
        name = data["name"]
        sql = data["sql"]

        dataset = Dataset.objects.get(id=datasetId)
        dataset.name = name
        dataset.sql = sql
        dataset.save()

        res.update(True, "Successfully updated dataset")
        return res

    @staticmethod
    def deleteDataset(datasetId: int):
        """
        Deletes a dataset
        :param datasetId: id of dataset
        """
        res = ApiResponse("Error in deleting dataset")
        dataset = Dataset.objects.get(id=datasetId)
        dataset.delete()

        res.update(True, "Successfully deleted dataset")
        return res

    @staticmethod
    def createDataset(data: dict):
        """
        Creates a dataset
        :param data: contains dataset name and sql
        """
        res = ApiResponse("Error in creating dataset")
        name = data["name"]
        sql = data["sql"]
        Dataset.objects.create(name=name, sql=sql)

        res.update(True, "Successfully created dataset")
        return res
