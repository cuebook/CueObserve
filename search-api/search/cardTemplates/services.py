import asyncio
import aiohttp
from flask import render_template_string
from search import app, db
from .models import SearchCardTemplate
from .serializer import SearchCardTemplateSchema
from elasticSearch.elastic_search_querying import ESQueryingUtils
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

    async def _sendDataRequest(session, dataUrl, payload):
        """
        Async method to fetch individual search card data
        :param session: ClientSession instance for aiohttp
        :param dataUrl: Url endpoint to fetch data
        :param payload: Dict containing parameters for fetching data
        """
        resp = await session.post(dataUrl, json=payload)
        responseData = await resp.json()
        return responseData

    async def fetchCardsData(dataUrl, searchResults):
        """
        Async method to fetch data for searched cards
        :param dataUrl: Url endpoint to fetch data
        :param searchResults: List of dicts containing search results
        """
        async with aiohttp.ClientSession() as session:
            result = await asyncio.gather(*(SearchCardTemplateServices._sendDataRequest(session, dataUrl, obj) for obj in searchResults))
            return result
    
    def getSearchCards(searchPayload: dict):
        """
        Service to fetch and create search cards on the fly
        :param searchPayload: Dict containing the search payload
        """
        # Temporary for testing # for globalDimensionValues only 
        gdValuesObjs = searchPayload.get("globalDimensionValuesPayload", [[]])
        globalDimensionId = gdValuesObjs[0].get("globalDimensionId", None)
        gdValues = gdValuesObjs[0].get("globalDimensionValue", [])
        globalDimensionValue = gdValues.get("name", "")

        searchResults = ESQueryingUtils.findGlobalDimensionResults(
            globalDimension = globalDimensionId,
            query = globalDimensionValue
        )
        
        searchTemplate = SearchCardTemplate.query.get(2) # Temporary for testing, will loop over templates, set here id accordingly
        for result in searchResults:
            result.update({"sqlTemplate": searchTemplate.sql})        

        dataResults = asyncio.run(SearchCardTemplateServices.fetchCardsData(DATASET_URL, searchResults))
        finalResults = []

        for i in range(len(searchResults)):
            finalResults.append(
                {
                    "title": render_template_string(searchTemplate.title, **searchResults[i]),
                    "text" : render_template_string(searchTemplate.bodyText, **searchResults[i]),
                    "data": dataResults[i]
                })
        
        return finalResults


        
    def getSearchSuggestions(query):
        app.logger.debug("Calling the query ES API and fetching only the top 10 results")
        data = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(
                    ESQueryingUtils.findGlobalDimensionResultsForSearchSuggestion,
                    query=query,
                    datasource=None,
                    offset=0,
                    limit=6,
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
                    # app.logger.info("data %s",data)
                except Exception as ex:
                    app.logger.error("Error in fetching search suggestions :%s", str(ex))
        
        res = {"success":True, "data":data}
        return res

