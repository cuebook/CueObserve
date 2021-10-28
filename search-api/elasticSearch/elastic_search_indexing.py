import os
import time
import logging
from typing import List, Dict
from collections import deque
from search import app
from elasticsearch import Elasticsearch
from elasticsearch.helpers import parallel_bulk
from datetime import datetime
from config import ELASTICSEARCH_URL
import threading
from .utils import Utils

import traceback


class ESIndexingUtils:
    """
    Class to handle Elastic Search related indexing
    and search utilities
    """
    GLOBAL_DIMENSIONS_NAMES_INDEX_NAME = "cueobserve_global_dimensions_names_for_search_index"
    GLOBAL_DIMENSIONS_INDEX_NAME = "global_dimensions_name_index_cueobserve"
    GLOBAL_DIMENSIONS_INDEX_DATA = "cueobserve_global_dimensions_data_index"
    GLOBAL_DIMENSIONS_INDEX_SEARCH_SUGGESTION_DATA = "cueobserve_global_dimensions_search_suggestion_data_index"
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
    def initializeIndex(indexName: str, indexDefinition: dict) -> str:
        """
        Method to name the index in Elasticsearch
        :indexName: the index name to be used for index creation
        :indexDefinition: the index definition - dict.
        """
        esClient = ESIndexingUtils._getESClient()
        logging.info("intializing Index here ...")
        currentIndexVersion = "_" + str(int(round(time.time() * 1000)))

        aliasIndex = indexName + currentIndexVersion
        logging.info("Creating index of: %s", aliasIndex)
        esClient.indices.create(index=aliasIndex, body=indexDefinition)

        return aliasIndex

    @staticmethod
    def ingestIndex(documentsToIndex: List[Dict], aliasIndex: str):
        """
        Method to ingest data into the index
        :param documentsToIndex The documents that need to be indexed.e.g,
        List of Cards or List of Global Dimensions
        :aliasIndex: the index name to be used for ingestion
        """
        esClient = ESIndexingUtils._getESClient()

        for documentToIndex in documentsToIndex:
            documentToIndex["_index"] = aliasIndex
            documentToIndex["_op_type"] = "index"
        logging.debug("Parallel indexing process starting.")

        deque(parallel_bulk(esClient, documentsToIndex), maxlen=0)

        logging.info("Alias index created at: %s", aliasIndex)

    @staticmethod
    def deleteOldIndex(indexName: str, aliasIndex: str):
        """
        Method to ingest data into the index
        :param documentsToIndex The documents that need to be indexed.e.g,
        List of Cards or List of Global Dimensions
        :aliasIndex: the index name to be used for ingestion
        """
        esClient = ESIndexingUtils._getESClient()

        logging.info("Now point the alias index: { %s } to  { %s }", aliasIndex, indexName)
        esClient.indices.put_alias(index=aliasIndex, name=indexName)

        logging.info("Now delete the older indices. They are of no use now.")
        # Now delete the older indices following a certain pattern.
        # Those indices are old indices and are of no use.
        allAliases = esClient.indices.get_alias("*")
        for key, value in allAliases.items():

            logging.debug("Checking for index: %s", key)
            # delete only the indexes matching the given pattern,
            # retain all the other indexes they may be coming from some other source
            if indexName in key:
                # do not delete the current index
                if aliasIndex == key:
                    continue

                logging.info("Deleting the index: %s", key)
                esClient.indices.delete(index=key, ignore=[400, 404])

    @staticmethod
    def _createIndex(documentsToIndex: List[Dict], indexName: str, indexDefinition: dict):
        """
        Method to create an index in Elasticsearch
        :param documentsToIndex The documents that need to be indexed.e.g,
        List of Cards or List of Global Dimensions
        :indexName: the index name to be used for index creation
        :indexDefinition: the index definition - dict.
        """

        aliasIndex = ESIndexingUtils.initializeIndex(indexName, indexDefinition)

        # ingest entries in the initialized index

        ESIndexingUtils.ingestIndex(documentsToIndex, aliasIndex)

        # at this stage index has been created at a new location
        # now change the alias of the main Index to point to the new index

        ESIndexingUtils.deleteOldIndex(indexName, aliasIndex)


    @staticmethod
    def fetchGlobalDimensionsForIndexing(globalDimensionGroup) :
        """
        Method to fetch the global dimensions and the dimension values.
        :return List of Documents to be indexed
        """
        indexingDocuments = []
        logging.info("global dimension group in fetch %s", globalDimensionGroup)
        globalDimensionName = globalDimensionGroup["name"]
        logging.debug("Starting fetch for global dimension: %s", globalDimensionName)
        globalDimensionId = globalDimensionGroup["id"]
        dimensionValues = globalDimensionGroup["values"]  # dimensional values

        logging.info("Merging dimensions Value percentile with mulitple vlaues in list of dimensionValues")
        for values in dimensionValues:

            displayValue = values["dimension"]
            dataset = values["dataset"]

            elasticsearchUniqueId = str(globalDimensionId) 

            document = {
                "_id": elasticsearchUniqueId,
                "globalDimensionName": str(globalDimensionName),
                "globalDimensionId": globalDimensionId,
            }
            indexingDocuments.append(document)
            logging.debug("Document to index: %s", document)

        return indexingDocuments
    @staticmethod
    def indexGlobalDimension():
        """
        Method to spawn a thread to index global dimension into elasticsearch existing indices
        The child thread assumes an index existing with a predefined unaltered indexDefinition
        """
        cardIndexer = threading.Thread(target=ESIndexingUtils.indexGlobalDimensionName)
        cardIndexer.start()

    @staticmethod
    def indexGlobalDimensionName(joblogger=None):
        """
        Method to index global dimensions data
        """
        logging.info("Fetching the global dimensions and the dimension values")
        response = Utils.getGlobalDimensionForIndex()
        logging.info("response of globaldimension value %s", response)
        if response["success"]:
            globalDimensions = response.get("data", [])
            logging.debug("Global dimensions: %s", globalDimensions)

            indexDefinition = {
                "settings": {
                    "analysis": {
                        "analyzer": {"my_analyzer": {"tokenizer": "my_tokenizer", "filter": ["lowercase"]}},
                        "default_search": {"type": "my_analyzer"},
                        "tokenizer": {
                            "my_tokenizer": {
                                "type": "edge_ngram",
                                "min_gram": 1,
                                "max_gram": 10,
                                "token_chars": ["letter", "digit"],
                            }
                        },
                    }
                },
                "mappings": {
                    "properties": {
                        "globalDimensionId": {"type": "integer"},
                        "globalDimensionName": {
                            "type": "text",
                            "search_analyzer": "my_analyzer",
                            "analyzer": "my_analyzer",
                            "fields": {"ngram": {"type": "text", "analyzer": "my_analyzer"}},
                        },
                    }
                },
            }

            indexName = ESIndexingUtils.GLOBAL_DIMENSIONS_NAMES_INDEX_NAME

            aliasIndex = ESIndexingUtils.initializeIndex(indexName, indexDefinition)
            app.logger.info("IndexName %s", indexName)
            app.logger.info("aliasIndex %s", aliasIndex)
            for globalDimensionGroup in globalDimensions:
                logging.info("globaldimensionGroup %s", globalDimensionGroup)
                # globalDimensionGroup is an array
                try:
                    documentsToIndex = ESIndexingUtils.fetchGlobalDimensionsForIndexing(
                        globalDimensionGroup
                    )

                    ESIndexingUtils.ingestIndex(documentsToIndex, aliasIndex)
                except (Exception) as error:
                    logging.error(str(error))
                    if joblogger:
                        joblogger.udpateSummary(
                            {
                                globalDimensionGroup[0]["globalDimension"]["name"]
                                + " stackTrace": traceback.format_exc()
                            }
                        )
                        joblogger.udpateSummary(
                            {globalDimensionGroup[0]["globalDimension"]["name"] + " message": str(error)}
                        )
                    pass

            ESIndexingUtils.deleteOldIndex(indexName, aliasIndex)

        else:
            logging.error("Error in fetching global dimensions.")
            raise RuntimeError("Error in fetching global dimensions")


    @staticmethod
    def fetchMeasureForIndexing():
        logging.info("Method to index cube measures")
        response = Utils.getMetricsFromCueObserve()
        data = []
        if (response.get("success", False)):
            logging.info("Get measure data for indexing")
            data = response.get("data",[])
        else:
            logging.error("Did not get Measure for Indexing")
            return 
        measureToBeIndex = []
        for res in data:
            dataset = res["dataset"]
            for measure in res.get("metrics",[]):

                measureToBeIndex.append(
                    {
                        "dataset": dataset,
                        "measure": measure,
                    }
                )
        logging.info("Sending the dataset measures for indexing")
        logging.debug("List to be indexed: %s", measureToBeIndex)
        ESIndexingUtils.indexMeasures(measureToBeIndex)


    @staticmethod
    def indexMeasures(documentsToIndex: List[Dict]):
        """
        Method to index the queries data
        :param documentsToIndex List of Queries metadata that needs to be indexed
        """
        logging.info("Starting indexing of measures and the associated metadata")

        indexDefinition = {
            "settings": {
                "analysis": {
                    "analyzer": {"my_analyzer": {"tokenizer": "my_tokenizer", "filter": ["lowercase"]}},
                    "default_search": {"type": "my_analyzer"},
                    "tokenizer": {
                        "my_tokenizer": {
                            "type": "edge_ngram",
                            "min_gram": 1,
                            "max_gram": 10,
                            "token_chars": ["letter", "digit"],
                        }
                    },
                }
            },
            "mappings": {
                "properties": {
                    "measure": {"type": "text"},
                    "dataset":{"type": "text"},
                }
            },
        }

        ESIndexingUtils._createIndex(
            documentsToIndex=documentsToIndex,
            indexName=ESIndexingUtils.DATASET_MEASURES_INDEX_NAME,
            indexDefinition=indexDefinition,
        )


    @staticmethod
    def fetchGlobalDimensionsValueForIndexing(globalDimensionGroup) :
        """
        Method to fetch the global dimensions and the dimension values.
        :return List of Documents to be indexed
        """
        indexingDocuments = []
        dimension = ''
        logging.info("global dimension group in fetch %s", globalDimensionGroup)
        globalDimensionName = globalDimensionGroup["name"]
        logging.debug("Starting fetch for global dimension: %s", globalDimensionName)
        globalDimensionId = globalDimensionGroup["id"]
        dimensionObjs = globalDimensionGroup["values"]  # dimensional values
        logging.info("Merging dimensions Value percentile with mulitple vlaues in list of dimensionValues")
        for dmObj in dimensionObjs:
            displayValue = ''
            dimension = dmObj["dimension"]
            dataset = dmObj["dataset"]
            datasetId = dmObj["datasetId"]
            res = Utils.getDimensionalValuesForDimension(datasetId, dimension)
            dimensionValues = res.get("data", [])
            if dimensionValues:
                for values in dimensionValues:
                    displayValue = values
                    elasticsearchUniqueId = str(globalDimensionId) + "_" + str(displayValue) + "_" + str(dataset)

                    document = {
                        "_id": elasticsearchUniqueId,
                        "globalDimensionValue": str(displayValue).lower(),
                        "globalDimensionDisplayValue": str(displayValue),
                        "globalDimensionName": str(globalDimensionName),
                        "globalDimensionId": globalDimensionId,
                        "dimension": dimension,
                        "dataset": dataset,
                        "datasetId": datasetId,
                    }
                    indexingDocuments.append(document)
                    logging.debug("Document to index: %s", document)

        return indexingDocuments
  

    @staticmethod
    def indexGlobalDimensionsData(joblogger=None):
        """
        Method to index global dimensions data
        """
        logging.info("Fetching the global dimensions and the dimension values")
        response = Utils.getGlobalDimensionForIndex()
        logging.info("response of globaldimension value %s", response)
        if response["success"]:
            globalDimensions = response.get("data", [])
            logging.debug("Global dimensions: %s", globalDimensions)

            indexDefinition = {
                "settings": {
                    "analysis": {
                        "analyzer": {"my_analyzer": {"tokenizer": "my_tokenizer", "filter": ["lowercase"]}},
                        "default_search": {"type": "my_analyzer"},
                        "tokenizer": {
                            "my_tokenizer": {
                                "type": "edge_ngram",
                                "min_gram": 1,
                                "max_gram": 10,
                                "token_chars": ["letter", "digit"],
                            }
                        },
                    }
                },
                "mappings": {
                    "properties": {
                        "globalDimensionId": {"type": "integer"},
                        "globalDimensionDisplayValue": {"type": "text"},
                        "globalDimensionValue": {
                            "type": "text",
                            "search_analyzer": "my_analyzer",
                            "analyzer": "my_analyzer",
                            "fields": {"ngram": {"type": "text", "analyzer": "my_analyzer"}},
                        },
                        "globalDimensionName": {
                            "type": "text",
                            "search_analyzer": "my_analyzer",
                            "analyzer": "my_analyzer",
                            "fields": {"ngram": {"type": "text", "analyzer": "my_analyzer"}},
                        },

                        "dimension": {
                            "type": "text",
                            "search_analyzer": "my_analyzer",
                            "analyzer": "my_analyzer",
                            "fields": {"ngram": {"type": "text", "analyzer": "my_analyzer"}},
                        },
                        "dataset": {"type": "text"},
                        "datasetId":{"type": "integer"},
                    }
                },
            }

            indexName = ESIndexingUtils.GLOBAL_DIMENSIONS_INDEX_DATA

            aliasIndex = ESIndexingUtils.initializeIndex(indexName, indexDefinition)
            print("indexName", indexName)
            print("alias index", aliasIndex)
            app.logger.info("IndexName %s", indexName)
            app.logger.info("aliasIndex %s", aliasIndex)
            for globalDimensionGroup in globalDimensions:
                logging.info("globaldimensionGroup %s", globalDimensionGroup)
                # globalDimensionGroup is an array
                try:
                    documentsToIndex = ESIndexingUtils.fetchGlobalDimensionsValueForIndexing(
                        globalDimensionGroup
                    )

                    ESIndexingUtils.ingestIndex(documentsToIndex, aliasIndex)
                except (Exception) as error:
                    logging.error(str(error))
                    if joblogger:
                        joblogger.udpateSummary(
                            {
                                globalDimensionGroup[0]["globalDimension"]["name"]
                                + " stackTrace": traceback.format_exc()
                            }
                        )
                        joblogger.udpateSummary(
                            {globalDimensionGroup[0]["globalDimension"]["name"] + " message": str(error)}
                        )
                    pass

            ESIndexingUtils.deleteOldIndex(indexName, aliasIndex)

        else:
            logging.error("Error in fetching global dimensions.")
            raise RuntimeError("Error in fetching global dimensions")


    @staticmethod
    def fetchGlobalDimensionsValueForSearchSuggestionIndexing(globalDimensionGroup) :       
        """
        Method to fetch the global dimensions and the dimension values.
        :return List of Documents to be indexed
        """
        indexingDocuments = []
        logging.info("global dimension group in fetch %s", globalDimensionGroup)
        globalDimensionName = globalDimensionGroup["name"]
        logging.debug("Starting fetch for global dimension: %s", globalDimensionName)
        globalDimensionId = globalDimensionGroup["id"]
        dimensionObjs = globalDimensionGroup["values"]  # dimensional values
        logging.info("Merging dimensions Value percentile with mulitple vlaues in list of dimensionValues")
        for dmObj in dimensionObjs:
            displayValue = ''
            dimension = dmObj["dimension"]
            dataset = dmObj["dataset"]
            datasetId = dmObj["datasetId"]
            res = Utils.getDimensionalValuesForDimension(datasetId, dimension)
            dimensionValues = res.get("data", [])
            if dimensionValues:
                for values in dimensionValues:
                    displayValue = values
                    elasticsearchUniqueId = str(globalDimensionId) + "_" + str(displayValue) 

                    document = {
                        "_id": elasticsearchUniqueId,
                        "globalDimensionValue": str(displayValue).lower(),
                        "globalDimensionDisplayValue": str(displayValue),
                        "globalDimensionName": str(globalDimensionName),
                        "globalDimensionId": globalDimensionId,
                        "dataset": dataset,
                        "datasetId": datasetId,
                    }
                    indexingDocuments.append(document)
                    logging.debug("Document to index: %s", document)

        return indexingDocuments
  

  # Below function is used for search suggestion / To avoid duplicates in search dropdown(Temparory)

    def indexGlobalDimensionsDataForSearchSuggestion(joblogger=None):
        """
        Indexing is being done for dropdown suggestion
        """
        logging.info("Fetching the global dimensions and the dimension values")
        response = Utils.getGlobalDimensionForIndex()
        logging.info("response of globaldimension value %s", response)
        if response["success"]:
            globalDimensions = response.get("data", [])
            logging.debug("Global dimensions: %s", globalDimensions)

            indexDefinition = {
                "settings": {
                    "analysis": {
                        "analyzer": {"my_analyzer": {"tokenizer": "my_tokenizer", "filter": ["lowercase"]}},
                        "default_search": {"type": "my_analyzer"},
                        "tokenizer": {
                            "my_tokenizer": {
                                "type": "edge_ngram",
                                "min_gram": 1,
                                "max_gram": 10,
                                "token_chars": ["letter", "digit"],
                            }
                        },
                    }
                },
                "mappings": {
                    "properties": {
                        "globalDimensionId": {"type": "integer"},
                        "globalDimensionDisplayValue": {"type": "text"},
                        "globalDimensionValue": {
                            "type": "text",
                            "search_analyzer": "my_analyzer",
                            "analyzer": "my_analyzer",
                            "fields": {"ngram": {"type": "text", "analyzer": "my_analyzer"}},
                        },
                        "globalDimensionName": {
                            "type": "text",
                            "search_analyzer": "my_analyzer",
                            "analyzer": "my_analyzer",
                            "fields": {"ngram": {"type": "text", "analyzer": "my_analyzer"}},
                        },
                        "dataset": {"type": "text"},
                        "datasetId":{"type": "integer"},
                    }
                },
            }

            indexName = ESIndexingUtils.GLOBAL_DIMENSIONS_INDEX_SEARCH_SUGGESTION_DATA

            aliasIndex = ESIndexingUtils.initializeIndex(indexName, indexDefinition)
            app.logger.info("IndexName %s", indexName)
            app.logger.info("aliasIndex %s", aliasIndex)
            for globalDimensionGroup in globalDimensions:
                logging.info("globaldimensionGroup %s", globalDimensionGroup)
                # globalDimensionGroup is an array
                try:
                    documentsToIndex = ESIndexingUtils.fetchGlobalDimensionsValueForSearchSuggestionIndexing(
                        globalDimensionGroup
                    )

                    ESIndexingUtils.ingestIndex(documentsToIndex, aliasIndex)
                except (Exception) as error:
                    logging.error(str(error))
                    if joblogger:
                        joblogger.udpateSummary(
                            {
                                globalDimensionGroup[0]["globalDimension"]["name"]
                                + " stackTrace": traceback.format_exc()
                            }
                        )
                        joblogger.udpateSummary(
                            {globalDimensionGroup[0]["globalDimension"]["name"] + " message": str(error)}
                        )
                    pass

            ESIndexingUtils.deleteOldIndex(indexName, aliasIndex)

        else:
            logging.error("Error in fetching global dimensions.")
            raise RuntimeError("Error in fetching global dimensions")