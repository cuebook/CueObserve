import asyncio
import aiohttp
from flask import render_template_string
from search import app, db
from models import SearchCardTemplate
from serializer import SearchCardTemplateSchema
from elasticSearch.elastic_search_querying import ESQueryingUtils
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
            result = await asyncio.gather(
                *(
                    SearchCardTemplateServices._sendDataRequest(session, dataUrl, {
                        "dataset": obj["dataset"],
                        "dimension": obj["dimension"],
                        "dimVal": obj["value"]
                    })
                        for obj in searchResults
                    )
                )
            return result
    
    def getSearchCards(searchPayload: dict):
        """
        Service to fetch and create search cards on the fly
        :param searchPayload: Dict containing the search payload
        """
        searchResults = ESQueryingUtils.findGlobalDimensionResults(
            query=searchPayload.get("query"),
            dataset=searchPayload.get("dataset"),
            globalDimension=searchPayload.get("globalDimension"),
            offset=searchPayload.get("offset", 0)
        )

        dataResults = asyncio.run(SearchCardTemplateServices.fetchCardsData(DATASET_URL, searchResults))
        searchTemplate = SearchCardTemplate.query.get(1) # Temporary for testing, will loop over templates

        finalResults = []

        for i in range(len(searchResults)):
            finalResults.append(
                {
                    "title": render_template_string(searchTemplate.title, **searchResults[i]),
                    "text" : render_template_string(searchTemplate.bodyText, **searchResults[i]),
                    "data": dataResults[i]
                })
        
        return finalResults

        
        

