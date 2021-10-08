import requests
from search import app
import logging
import json
from flask import Flask, request, jsonify, make_response
from search.globalDimensions import  createGlobalDimension, getDimensionFromCueObserve, getGlobalDimensions
# app = Flask(__name__)


@app.route("/search/globalDimension/create/", methods=['POST'])
def createGlobalDimensionView():
    app.logger.info("json %s", request.json)
    payloads = request.json
    res1 = createGlobalDimension(payloads)
    res = {"success": True}
    # app.logger.info("json %s", res)

    return jsonify(res)

@app.route("/search/dimension/", methods=['GET', 'POST', 'OPTIONS'])
def getDimensions():
    app.logger.info("request.header %s", request.headers)
    res = getDimensionFromCueObserve()
    return jsonify(res)

@app.route("/search/global-dimension/", methods=["GET"])
def getGlobalDimensionsView():
    app.logger.info("Requests for Global Dimension ")
    res = getGlobalDimensions()
    return jsonify(res)


