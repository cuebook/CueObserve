
from search import app
from flask import Flask, request, jsonify, make_response

from .services import SearchCardTemplateServices

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