from search import app
import json
from flask import Flask, request, jsonify, make_response
from search.globalDimensions import getGlobalDimensions, createGlobalDimension
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
    app.logger.info("request header %s", request.headers)
    res = jsonify({"success": True})
    return res

