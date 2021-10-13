import requests
from search import app, db
from models import SearchCardTemplate
from serializer import SearchCardTemplateSchema
from config import DATASET_URL

class SearchCardTemplateServices:
    """
    Service for various Card template operations
    """
    def getCardTemplates():
        """
        Service to fetch all card templates
        """
        try:
            app.logger.info("Getting card templates")
            templates = SearchCardTemplate.query.all()
            data = SearchCardTemplateSchema(many=True).dump(templates)
            return data

        except Exception as ex:
            app.logger.error(f"Failed to get card templates {ex}")
            return []
    
    def getSearchCards(searchPayload: dict):
        """
        Service to fetch and create search cards on the fly
        :param searchPayload: Dict containing the search payload
        """
        searchResults = [] # Insert ES Querying here
        datasetIds = list(set([result["datasetId"] for result in searchResults]))

        datasetDfs = {}

        for datasetId in datasetIds:
            response = requests.post(DATASET_URL, data={"datasetId": datasetId})
            datasetDfs[datasetId] = response.json().get("dfDict", [])
        
        

