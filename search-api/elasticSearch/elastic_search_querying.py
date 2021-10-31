import logging
import os
from typing import List
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from config import ELASTICSEARCH_URL

class ESQueryingUtils:

    GLOBAL_DIMENSIONS_INDEX_SEARCH_SUGGESTION_DATA = "cueobserve_global_dimensions_search_suggestion_data_index"
    GLOBAL_DIMENSIONS_NAMES_INDEX_NAME = "cueobserve_global_dimensions_names_for_search_index"
    GLOBAL_DIMENSIONS_INDEX_DATA = "cueobserve_global_dimensions_data_index"
    DATASET_MEASURES_INDEX_NAME = "dataset_measures_index_cueobserve"

    @staticmethod
    def _getESClient() -> Elasticsearch:
        """
        Method to get the ES Client
        """
        esHost = ELASTICSEARCH_URL
        esClient = Elasticsearch(hosts=[esHost])
        return esClient

    @staticmethod
    def findGlobalDimensionResults(
        query: str, datasource = None, globalDimension: int = None, offset: int = 0, limit: int = 5
    ) :
        """
        Method to run search queries on GlobalDimensions
        :param query: User search query
        :param dataset: name of cube, will match values associated
                 to global dimension associated with this cube
        :param offset: Offset for the query
        :param limit: Number of results required
        :return List[ESQueryResponse]
        """
        globalDimensionNameQuery = None
        if len(query.split(":")) == 2:
            globalDimensionNameQuery = query.split(":")[0]
            query = query.split(":")[1]

        logging.info("Querying global dimensions for: %s", query)

        query = "" if query is None else query.lower()
        client = ESQueryingUtils._getESClient()

        searchQuery = Search(index=ESQueryingUtils.GLOBAL_DIMENSIONS_INDEX_DATA).using(client)

        if globalDimension:
            searchQuery = searchQuery.filter("match", globalDimensionId=globalDimension)
        elif globalDimensionNameQuery:
            searchQuery = searchQuery.filter("match", globalDimensionName=globalDimensionNameQuery)

        if query:
            searchQuery = searchQuery.query("match", globalDimensionValue=query)
        else:
            searchQuery = searchQuery.query("match_all")

        if datasource:
            searchQuery = searchQuery.filter("match", cubes=datasource)
        searchQuery = searchQuery[offset : offset + limit]

        logging.info("Calling Elasticsearch with the query")
        response = searchQuery.execute()

        output = []
        for hit in response:
            obj = {
                "value": hit.globalDimensionDisplayValue,
                "dimension": hit.dimension,
                "globalDimensionName": hit.globalDimensionName,
                "user_entity_identifier": hit.globalDimensionName,
                "id": hit.globalDimensionId,
                "dataset": hit.dataset,
                "datasetId": hit.datasetId,
                "type": "GLOBALDIMENSION",
            }
            output.append(obj)

        logging.debug("User queries: %s", output)
        return output
    @staticmethod
    def findGlobalDimensionNames(
        query: str, datasource: str = None, offset: int = 0, limit: int = 5
    ) :
        """
        Method to index the global dimension names for search.
        For e.g. G_City, G_Product, etc.
        To be used in search for e.g. - G_City = Mumbai, G_Product = Nike
        :param query: str
        :param datasource: name of cube, will match values associated with this cube
        :param offset: Offset for the query
        :param limit: Number of results required
        :return List[ESQueryResponse]
        """
        logging.info("Querying the global dimensions names index")
        client = ESQueryingUtils._getESClient()

        searchQuery = (
            Search(index=ESQueryingUtils.GLOBAL_DIMENSIONS_NAMES_INDEX_NAME)
            .using(client)
            .query("multi_match", query=query, fields=["globalDimensionName"])
        )

        if datasource:
            searchQuery = searchQuery.filter("match", cubes=datasource)

        searchQuery = searchQuery[offset : offset + limit]

        logging.info("Calling Elasticsearch with the query")
        response = searchQuery.execute()

        output = []
        for hit in response:
            obj = {
                "value": hit.globalDimensionName,
                "user_entity_identifier": "DIMENSION",
                "id": hit.globalDimensionId,
                "type": "DIMENSION",
            }
            output.append(obj)

        logging.debug("Global dimensions: %s", output)
        return output

    
    @staticmethod
    def findQueries(query: str):
        """
        Method to run the search query on the queries Index
        :param query str
        :return List[ESQueryResponse]
        """
        logging.info("Querying the Queries Index")
        client = ESQueryingUtils._getESClient()

        searchQuery = (
            Search(index=ESQueryingUtils.GLOBAL_DIMENSIONS_INDEX_DATA)
            .using(client)
            .query("multi_match", query=query, fields=["globalDimensionName"])
        )

        logging.info("Calling Elasticsearch with the query")
        response = searchQuery.execute()

        output = []
        for hit in response:
            obj = {
                "value": hit.globalDimensionDisplayValue,
                "user_entity_identifier": hit.globalDimensionName,
                "id": hit.globalDimensionId,
                "type": "DIMENSION",
                "dataset": hit.dataset,
            }
            output.append(obj)

        logging.debug("Queries: %s", output)
        return output
####################### Used for searchSuggestion query ########################

    @staticmethod
    def findGlobalDimensionResultsForSearchSuggestion(
        query: str, datasource = None, globalDimension: int = None, offset: int = 0, limit: int = 5
    ) :
        """
        Method to run search queries on GlobalDimensions
        :param query: User search query
        :param dataset: name of cube, will match values associated
                 to global dimension associated with this cube
        :param offset: Offset for the query
        :param limit: Number of results required
        :return List[ESQueryResponse]
        """
        globalDimensionNameQuery = None
        if len(query.split(":")) == 2:
            globalDimensionNameQuery = query.split(":")[0]
            query = query.split(":")[1]

        logging.info("Querying global dimensions for: %s", query)

        query = "" if query is None else query.lower()
        client = ESQueryingUtils._getESClient()

        searchQuery = Search(index=ESQueryingUtils.GLOBAL_DIMENSIONS_INDEX_SEARCH_SUGGESTION_DATA).using(client)

        if globalDimension:
            searchQuery = searchQuery.filter("match", globalDimensionId=globalDimension)
        elif globalDimensionNameQuery:
            searchQuery = searchQuery.filter("match", globalDimensionName=globalDimensionNameQuery)

        if query:
            searchQuery = searchQuery.query("match", globalDimensionValue=query)
        else:
            searchQuery = searchQuery.query("match_all")

        if datasource:
            searchQuery = searchQuery.filter("match", cubes=datasource)
        searchQuery = searchQuery[offset : offset + limit]

        logging.info("Calling Elasticsearch with the query")
        response = searchQuery.execute()

        output = []
        for hit in response:
            obj = {
                "value": hit.globalDimensionDisplayValue,
                "user_entity_identifier": hit.globalDimensionName,
                "id": hit.globalDimensionId,
                "type": "GLOBALDIMENSION",
            }
            output.append(obj)

        logging.debug("User queries: %s", output)
        return output
    