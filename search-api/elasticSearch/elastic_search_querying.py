import logging
import os
from typing import List
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from config import ELASTICSEARCH_URL

class ESQueryingUtils:


    GLOBAL_DIMENSIONS_INDEX_NAME = "global_dimensions_index_cueobserve"

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
        query: str, dataset=None, globalDimension: int = None, offset: int = 0, limit: int = 5
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

        searchQuery = Search(index=ESQueryingUtils.GLOBAL_DIMENSIONS_INDEX_NAME).using(client)

        if globalDimension:
            searchQuery = searchQuery.filter("match", globalDimensionId=globalDimension)
        elif globalDimensionNameQuery:
            searchQuery = searchQuery.filter("match", globalDimensionName=globalDimensionNameQuery)

        if query:
            searchQuery = searchQuery.query("match", globalDimensionValue=query)
        else:
            searchQuery = searchQuery.query("match_all")

        if dataset:
            searchQuery = searchQuery.filter("match", dataset=dataset)
        searchQuery = searchQuery[offset : offset + limit]

        logging.info("Calling Elasticsearch with the query")
        response = searchQuery.execute()

        output = []
        for hit in response:
            obj = {
                "value": hit.globalDimensionDisplayValue,
                "dimension": hit.globalDimensionName,
                "user_entity_identifier": hit.globalDimensionName,
                "id": hit.globalDimensionId,
                "type": "GLOBALDIMENSION",
                "dataset": hit.dataset,
                
            }
            output.append(obj)
        logging.info("output %s", output)
        logging.debug("User queries: %s", output)
        return output