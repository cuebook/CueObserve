
from search import app
from flask import Flask, request, jsonify, make_response

from .services import SearchCardTemplateServices
from elasticSearch import ESIndexingUtils

@app.route("/search/cardTemplates/", methods=["GET"])
def getCardTemplates():
    app.logger.info("Requests for Card Templates ")
    res = SearchCardTemplateServices.getCardTemplates()
    return jsonify(res)

@app.route("/search/getCards/", methods=['POST'])
def getSearchCards():
    app.logger.info("Fetching cards for search")
    payload = request.json
    res = SearchCardTemplateServices.getSearchCards(payload)
    return jsonify(res)


@app.route("/search/searchsuggestions/", methods=['POST'])
def getSearchSuggestionsView():
    app.logger.info("Fetching cards for search")
    searchQuery = request.json
    res = SearchCardTemplateServices.getSearchSuggestions(searchQuery)
    return jsonify(res)


@app.route("/search/runIndexing/", methods=['GET'])
def elasticSearchIndexingView():
    ESIndexingUtils.indexGlobalDimensionName()
    ESIndexingUtils.indexGlobalDimensionsData()
    res = {"success":True, "message":"indexing completed !"}
    return jsonify(res)
