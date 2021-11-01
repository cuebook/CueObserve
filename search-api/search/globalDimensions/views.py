import requests
from search import app
import logging
import json
from flask import Flask, request, jsonify, make_response
from .services import GlobalDimensionServices

@app.route("/search/global-dimension/create/", methods=['POST'])
def createGlobalDimensionView():
    payloads = request.json
    res = GlobalDimensionServices.createGlobalDimension(payloads)
    return jsonify(res)

@app.route("/search/global-dimension/delete/<int:id>", methods=['DELETE'])
def deleteGlobalDimensionView(id):
    res = GlobalDimensionServices.deleteGlobalDimension(id)
    return jsonify(res)


@app.route("/search/dimension/", methods=['GET'])
def getDimensions():
    res = GlobalDimensionServices.getDimensionFromCueObserve()
    return jsonify(res)

# Use it, when need it on UI
# @app.route("/search/metrics/", methods=['GET'])
# def getMetrics():
#     app.logger.info("Get all metrics from CueObserve ")
#     res = getMetricsFromCueObserve()
#     return jsonify(res)

@app.route("/search/global-dimension/", methods=["GET"])
def getGlobalDimensionsView():
    res = GlobalDimensionServices.getGlobalDimensions()
    return jsonify(res)

@app.route("/search/global-dimension/publish", methods=["POST"])
def updateGlobalDimension():
    payload = request.json
    res = GlobalDimensionServices.publishGlobalDimension(payload)
    return jsonify(res)

@app.route("/search/global-dimension/<int:id>", methods=["GET"])
def getGlobalDimensionView(id):
    res = GlobalDimensionServices.getGlobalDimensionById(id)
    return jsonify(res)

@app.route("/search/global-dimension/update/<int:id>", methods=["POST"])
def updateGlobalDimensionView(id):
    payload = request.json
    res = GlobalDimensionServices.updateGlobalDimensionById(id, payload)
    return jsonify(res)
