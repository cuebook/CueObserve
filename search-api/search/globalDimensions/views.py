from search import app
import json
from flask import Flask, request, jsonify
from search.globalDimensions import getGlobalDimensions, createGlobalDimension
# app = Flask(__name__)

@app.route("/search/global-dimension/", methods=["GET",'POST'])
def getGlobalDimensionsView():
    app.logger.info("methods %s", request.method)
    payloads = json.loads(request.data.decode("UTF-8"))
    app.logger.info("data %s", payloads)
    res = getGlobalDimensions(payloads)

    return jsonify(res)



@app.route("/search/global-dimension/create/", methods=['GET','POST'])
def createGlobalDimensionView():
    app.logger.info("request %s", request.method)
    # res = createGlobalDimension(request.data)

    return {"success":"true"}