import requests
from search import app
import logging
import json
from flask import Flask, request, jsonify, make_response
from search.globalDimensions import getGlobalDimensions, createGlobalDimension, getDimensionFromCueObserve
from flask_apispec import use_kwargs
# app = Flask(__name__)

@app.route("/search/global-dimension/", methods=["GET", 'POST'])
def getGlobalDimensionsView():
    app.logger.info("methods %s", request.headers)
    payloads = json.loads(request.data.decode("UTF-8"))
    app.logger.info("data %s", payloads)
    res = getGlobalDimensions(payloads)
    return jsonify(res)


@app.route("/search/globalDimension/create/", methods=['GET', 'POST', 'OPTIONS'])
def createGlobalDimensionView():
    # app.logger.info("request header %s", dir(request))
    # app.logger.info("request form %s", type(request.data.decode("UTF-8")))
    
    app.logger.info("json %s", request.json)
    # logging.warning("json %s", request.json["name"])

    # payloads = request.data.decode('UTF-8')
    
    # app.logger.info("paylodas load %s", kwargs)
    # app.logger.info("payloads  %s", payloads)
    # app.logger.info("payloads  %s", type(payloads))
    # app.logger.info("payloads  %s", payloads.get("name"))

    # app.logger.info("payloads  %s", payloads['name'])
    # app.logger.info("payloads  %s", type(payloads))

    # app.logger.info("payloads  %s", payloads.get('name'))


    # l = createGlobalDimension(payloads)
    res = {"success": True}
    # app.logger.info("json %s", res)

    return jsonify(res)

@app.route("/search/dimension/", methods=['GET'])
def getDimensions():
    app.logger.info("request.header %s", request.headers)
    res = getDimensionFromCueObserve()
    return jsonify(res)
