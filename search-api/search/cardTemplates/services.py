import requests
from search import app, db
from .models import SearchCardTemplate
from .serializer import SearchCardTemplateSchema
from config import DATASET_URL
import concurrent.futures
from elasticSearch import ESQueryingUtils, ESIndexingUtils

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

        # for datasetId in datasetIds:
        #     response = requests.post(DATASET_URL, data={"datasetId": datasetId})
        #     datasetDfs[datasetId] = response.json().get("dfDict", [])
        results = []
        for i in range(3):
            resDicts = {}
            resDicts["Title"] = "card " + str(i)
            resDicts["Text"] = "Test for card table and filter is delhi card id is : " + str(i)
            resDicts["data"] = [1,2,3,4,5,6]
            results.append(resDicts)

        res = {"success":True, "searchCards":results}
        return res

        
    def getSearchSuggestions(query):
        app.logger.debug("Calling the query ES API and fetching only the top 10 results")
        data = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    ESQueryingUtils.findGlobalDimensionResults,
                    query=query,
                    datasource=None,
                    offset=0,
                    limit=4,
                ),
                executor.submit(
                    ESQueryingUtils.findGlobalDimensionNames,
                    query=query,
                    datasource=None,
                    offset=0,
                    limit=4,
                ),
            ]

            for future in concurrent.futures.as_completed(futures):
                try:
                    data.extend(future.result())
                    app.logger.info("data %s",data)
                    app.logger.info("data after reverse sortign %s", data)
                except Exception as ex:
                    app.logger.error("Error in fetching search suggestions :%s", str(ex))
        
        app.logger.debug("Fetched results: %s", data)
        res = {"success":True, "data":data}
        return res

