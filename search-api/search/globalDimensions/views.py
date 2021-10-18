import requests
from search import app
import logging
import json
from flask import Flask, request, jsonify, make_response
from search.globalDimensions import  createGlobalDimension, getDimensionFromCueObserve, getGlobalDimensions, updateGlobalDimensionById, getMetricsFromCueObserve, publishGlobalDimension, getGlobalDimensionById
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

@app.route("/search/publish/global-dimension", methods=["POST"])
def updateGlobalDimension():
    payload = request.json
    app.logger.info("payload %s", payload)
    res = publishGlobalDimension(payload)
    return jsonify(res)

@app.route("/search/global-dimension/<int:id>", methods=["GET"])
def getGlobalDimensionView(id):
    app.logger.info("Requests for Global Dimension ", id)
    res = getGlobalDimensionById(id)
    return jsonify(res)

@app.route("/search/update/global-dimension/<int:id>", methods=["POST"])
def updateGlobalDimensionView(id):
    payload = request.json
    res = updateGlobalDimensionById(id, payload)
    return jsonify(res)
