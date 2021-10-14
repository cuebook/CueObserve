import requests
from search import app
import logging
import json
from flask import Flask, request, jsonify, make_response
from search.globalDimensions import  createGlobalDimension, getDimensionFromCueObserve, getGlobalDimensions, getMetricsFromCueObserve
# app = Flask(__name__)


@app.route("/search/globalDimension/create/", methods=['POST'])
def createGlobalDimensionView():
    app.logger.info("Procedure starts for creating global dimension ")
    payloads = request.json
    res = createGlobalDimension(payloads)
    return jsonify(res)

@app.route("/search/dimension/", methods=['GET'])
def getDimensions():
    app.logger.info("Get dimension from CueObserve ")
    res = getDimensionFromCueObserve()
    return jsonify(res)

# Use it, when need it on UI
# @app.route("/search/metrics/", methods=['GET'])
# def getMetrics():
#     app.logger.info("Get all metrics from CueObserve ")
#     res = getMetricsFromCueObserve()
#     return jsonify(res)

@app.route("/search/global-dimension/", methods=["GET"])
def getGlobalDimensionsView():
    app.logger.info("Requests for Global Dimension ")
    res = getGlobalDimensions()
    return jsonify(res)


